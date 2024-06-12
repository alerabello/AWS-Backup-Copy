# AWS Backup Copy Lambda

Este é um lambda function para copiar os recovery points do AWS Backup de um ou mais vaults em diferentes regiões para um vault em outra região.

## Configuração

### IAM Role e KMS KEY

Certifique-se de que o IAM Role associado à função Lambda tenha permissões suficientes para realizar as operações necessárias, como listar recovery points, iniciar jobs de cópia e verificar o status dos jobs.
Certifique-se de que todos os dados estão com KMS KEY, inclusive os Vault e que estão compartilhados entre contas.

### Configurações Específicas

- `regions`: Uma lista de regiões onde os vaults de origem estão localizados.
- `destination_region`: A região onde o vault de destino está localizado.
- `source_backup_vault_names`: Um dicionário mapeando as regiões aos nomes dos vaults de origem.
- `destination_backup_vault_name`: O nome do vault de destino.
- `iam_role_arn`: O ARN do IAM Role usado para realizar operações de cópia.

### Substituições Necessárias:
- `nome_do_vault_sa_east_1`: Substitua pelo nome real do vault na região sa-east-1.
- `nome_do_vault_us_east_1`: Substitua pelo nome real do vault na região us-east-1.
- `nome_do_vault_eu_central_1`: Substitua pelo nome real do vault na região eu-central-1.
- `arn:aws:iam::00000000000:role/nome_do_iam_role`: Substitua pelo ARN real do IAM Role.

## Como Usar

1. Clone este repositório:
2. Faça as modificações necessárias no código, como configurar os nomes dos vaults e o ARN do IAM Role.
3. Implante a função Lambda na AWS.
4. Configure um evento agendado para acionar a função Lambda diariamente às 07:00.

## Contribuição

Contribuições são bem-vindas! Abra um issue ou envie um pull request com melhorias ou correções.


- ` Esse código garantirá que apenas os recovery points criados no dia atual sejam copiados dos vaults nas regiões sa-east-1 e us-east-1 para o vault na região eu-central-1.`
- ` Cuidado com custos de data transfer.`

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
