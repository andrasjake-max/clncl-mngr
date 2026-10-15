# Sistema de Atendimento em Clinicas - INE5605 Trabalho 1

Sistema orientado a objetos em Python (MVC) para gerenciar clinicas,
pacientes, profissionais de saude, atendimentos, procedimentos e pagamentos.

## Como executar

```
python main.py
```

## Testes

Testes automatizados das 4 regras do enunciado (idade, horario da clinica,
data do pagamento e pagamentos parciais), com `unittest` da biblioteca padrao:

```
python -m unittest -v
```

## Estrutura (MVC)

| Pacote        | Papel                                                            |
|---------------|------------------------------------------------------------------|
| `entidade/`   | Modelo: classes de dominio e validacao dos dados                 |
| `limite/`     | Visao: telas (entrada e saida pelo terminal)                     |
| `controle/`   | Controladores: regras de negocio, ligam telas e entidades        |
| `exceptions/` | Excecoes do sistema (todas herdam de `SistemaException`)         |
| `UML/`        | Diagramas de classes UML (`.drawio` editavel + PNG exportado)    |

## Conceitos de OO usados

- **Heranca + classe abstrata:** `Pessoa` -> `Paciente`, `ProfissionalSaude`;
  `Pagamento` -> `PagamentoDinheiro`, `PagamentoPix`, `PagamentoCartao`;
  `TelaAbstrata` -> todas as telas; `SistemaException` -> excecoes do sistema.
- **Composicao:** `Atendimento` <>-- `Procedimento` (o procedimento e criado pelo
  atendimento e excluido junto com ele).
- **Agregacao:** `Clinica` <>-- `ProfissionalSaude` (o profissional existe sem
  a clinica e pode atender em varias).
- **Associacao:** `Atendimento` -> `Clinica`, `Paciente`, `ProfissionalSaude`,
  `TipoAtendimento`; `Pagamento` -> `Atendimento`; `Paciente` -> responsavel.

## Regras de negocio implementadas

1. Paciente menor de 18 anos so e atendido se tiver responsavel maior de idade.
2. Atendimento deve estar dentro do horario de funcionamento da clinica.
3. Pagamento deve ser feito ate a data do atendimento.
4. Pagamento em dinheiro, PIX (CPF do pagador) ou cartao (numero e bandeira).
5. Pagamentos parciais permitidos; o valor restante e calculado
   (valor do atendimento + custo dos procedimentos - total pago).
6. Extras: profissional precisa estar vinculado a clinica; sem conflito de
   horario para profissional/paciente; nao exclui registros em uso.
