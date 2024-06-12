import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Verifica se a hora atual é após as 07h00
    current_time = datetime.now().time()
    if current_time < datetime.strptime('07:00:00', '%H:%M:%S').time():
        return {
            'statusCode': 400,
            'body': 'A cópia só pode ser iniciada após as 07h00.'
        }

    # Configurações dos vaults, regiões e IAM Role
    regions = ['sa-east-1', 'us-east-1']
    destination_region = 'eu-central-1'
    source_backup_vault_names = {
        'sa-east-1': 'nome_do_vault_sa_east_1',
        'us-east-1': 'nome_do_vault_us_east_1'
    }
    destination_backup_vault_name = 'nome_do_vault_eu_central_1'
    iam_role_arn = 'arn:aws:iam::00000000000:role/nome_do_iam_role'

    # Inicializa os clientes para AWS Backup nas regiões de origem e destino
    backup_clients = {region: boto3.client('backup', region_name=region) for region in regions}
    destination_backup_client = boto3.client('backup', region_name=destination_region)

    # Calcula a data de início e fim para os recovery points do dia atual
    today = datetime.now().date()

    # Inicializa uma lista para armazenar os IDs dos jobs de cópia
    copy_job_ids = []

    # Função para listar e copiar recovery points
    def list_and_copy_recovery_points(region, backup_vault_name):
        paginator = backup_clients[region].get_paginator('list_recovery_points_by_backup_vault')
        for page in paginator.paginate(BackupVaultName=backup_vault_name):
            for recovery_point in page['RecoveryPoints']:
                recovery_point_creation_date = recovery_point['CreationDate'].date()
                if recovery_point_creation_date == today:
                    # Inicia um copy job para copiar o recovery point para o vault de destino
                    copy_job = backup_clients[region].start_copy_job(
                        RecoveryPointArn=recovery_point['RecoveryPointArn'],
                        SourceBackupVaultName=backup_vault_name,
                        DestinationBackupVaultArn=destination_backup_client.describe_backup_vault(BackupVaultName=destination_backup_vault_name)['BackupVaultArn'],
                        IamRoleArn=iam_role_arn
                    )
                    copy_job_ids.append(copy_job['CopyJobId'])

    # Listar e copiar recovery points para cada região e vault de origem
    for region, backup_vault_name in source_backup_vault_names.items():
        list_and_copy_recovery_points(region, backup_vault_name)

    # Verifica periodicamente o status dos jobs de cópia
    for copy_job_id in copy_job_ids:
        while True:
            try:
                copy_job_status = destination_backup_client.describe_copy_job(CopyJobId=copy_job_id)
                if 'State' not in copy_job_status:
                    return {
                        'statusCode': 500,
                        'body': f'O job de cópia {copy_job_id} não retornou um estado válido.'
                    }
                if copy_job_status['State'] == 'COMPLETED':
                    break
                elif copy_job_status['State'] == 'FAILED':
                    return {
                        'statusCode': 500,
                        'body': f'Falha ao copiar o recovery point com o job {copy_job_id}.'
                    }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': f'Erro ao verificar o status do job de cópia {copy_job_id}: {str(e)}'
                }

    return {
        'statusCode': 200,
        'body': 'Cópia dos recovery points do dia atual iniciada com sucesso.'
    }