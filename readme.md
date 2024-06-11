# AWS Backup Copy Lambda

Este é um lambda function para copiar os recovery points do AWS Backup de um ou mais vaults em diferentes regiões para um vault em outra região.

## Configuração

### IAM Role

Certifique-se de que o IAM Role associado à função Lambda tenha permissões suficientes para realizar as operações necessárias, como listar recovery points, iniciar jobs de cópia e verificar o status dos jobs.

### Variáveis de Ambiente

Antes de implantar a função Lambda, defina as seguintes variáveis de ambiente:

- `AWS_DEFAULT_REGION`: A região padrão onde a função Lambda será executada.
- `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`: Credenciais com permissões adequadas para acessar os serviços AWS necessários.

### Configurações Específicas

- `regions`: Uma lista de regiões onde os vaults de origem estão localizados.
- `destination_region`: A região onde o vault de destino está localizado.
- `source_backup_vault_names`: Um dicionário mapeando as regiões aos nomes dos vaults de origem.
- `destination_backup_vault_name`: O nome do vault de destino.
- `iam_role_arn`: O ARN do IAM Role usado para realizar operações de cópia.

## Como Usar

1. Clone este repositório:
2. Faça as modificações necessárias no código, como configurar os nomes dos vaults e o ARN do IAM Role.
3. Implante a função Lambda na AWS.
4. Configure um evento agendado para acionar a função Lambda diariamente às 07:00.

## Contribuição
Contribuições são bem-vindas! Abra um issue ou envie um pull request com melhorias ou correções.

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
