# File Organizer escrito em Python
Classes para ajudá-lo a organizar sua pasta de Downloads ou qualquer outra.
O sistema permite que você insira uma instância de RulesMap, que requer um diretório raiz (o qual será organizado) e um dicionário simples para que o Organizador conheça suas preferências.
Veja na sessão abaixo como funciona um RulesMap mais detalhadamente.

## Entendendo um RulesMap
O mapa é muito simples e intuitivo! Como já foi dito logo acima, ele requer apenas um diretório que será o alvo da organização e um dicionário. 
Ele segue um padrão de `extensão: pasta de destino`. Pode parecer um pouco complexo, mas é apenas um simples dicionário. Veja um exemplo:

```python
...
rules = {
  'png': 'Images',
  'jpeg': 'Images',
  'gif': 'Gif Images',
  'exe': '.*E* Files'
}
...
```
Viu como é simples? Você apenas insere a extensão como chave e a pasta de destino como o valor. Outro truque interessante é adicionar as expressões `*E*` e `*e*` nas chaves do seu mapa. A primeira, se diferenciando por sua letra em maiúsculas, é substituida pela extensão do arquivo totalmente em maiúsculas, enquanto sua prima, a segunda, é substituida pela extensão do arquivo em minúsculas. Veja abaixo um código que lhe ajuda a entender esse recurso.

```python
...
rules = {
  ...
  'gif': '*e* Images' -> 'gif Images'
  'exe': '.*E* Files' -> '.EXE Files'
}
...
```
_This Python code is not valid and is used only to exemplify the features_

Mas, à princípio, isso não parece muita coisa, certo? Já que nesse caso você poderia inserir diretamente a extensão da forma que achar melhor. Isso, pois esse recurso foi criado com o objetivo de melhorar a organização para as extensões não especificadas no mapa. Um RulesMap à princípio determina que o Organizador deve ignorar arquivos encontrados que não contenham uma extensão conhecida pelas regras inseridas, mas isso pode ser mudado ao alterar o valor da propriedade `skip_unknown_exts` para `False`. Ao fazer isso, o Organizador moverá os arquivos desconhecidos para pastas com base na sintaxe da propriedade `unknown_ext_format` que vem como `*E* Files` por padrão.

## Entendendo o Organizador
Primeiramente, ao menos por enquanto, o Organizador não suporta a leitura e processo de subdiretórios, embora você possa instânciar um Organizador para cada subdiretório que desejar. Além disso, ele trabalha diretamente na Thread principal.

O Organizador obtém e em seguida percorre todos os arquivos dentro do diretório especificado, assim, buscando uma correspondência entre a extensão do arquivo atual e as chaves do mapa, para assim, encontrar a pasta de destino determinada. Quando não há nenhuma correspondência, se a propriedade `skip_unknown_exts` for igual a `False`, ele moverá o arquivo para uma pasta com nome baseado na sintaxe da propriedade `unknown_ext_format` do mapa, do contrário o arquivo será ignorado e não será movido.

## RulesMap padrão
Você pode usar um RulesMap padrão importando do arquivo `rule_maps.py` a constante `BASIC_MAP`. No entanto, ele vem todo em inglês. Se você quiser personalizado para o português, basta seguir o passo-a-passo na sessão *Entendendo um RulesMap*.

## Exemplos de Uso
Veja abaixo alguns exemplos de uso do Organizador:

**Usando um RulesMap padrão**
```python
from organizer import RulesMap, Organizer
from rule_maps import BASIC_MAP

# Creating a RulesMap
rm = RulesMap(r'C:\Users\jwesleylima\Downloads', BASIC_MAP)

# Creating an Organizer
org = Organizer(rm)
org.organize()
```
**Criando meu RulesMap**
```python
from organizer import RulesMap, Organizer

# Creating custom rules
rules = {
  # media
  'png': 'Images',
  'jpg': 'Images',
  'mp4': 'Videos',
  # programming
  'py': 'Python Sources',
  'html': 'HTML Documents',
  'java': 'Java Sources'
}
# Creating a RulesMap
rm = RulesMap(r'C:\Users\jwesleylima\LargeFolder', rules)

# Creating an Organizer
org = Organizer(rm)
org.organize()
```
**Criando meu RulesMap à partir de um documento JSON**

Primeiramente, imagine que temos o seguinte documento JSON em nosso diretório raiz:

```javascript
{
  "md": "MarkDown Documents",
  "gitignore": "Git Ignore Files"
}
```

Agora vamos usá-lo como regras para nosso RulesMap:

```python
from organizer import RulesMap, Organizer

# Creating a custom RulesMap
rm = RulesMap.from_json(r'C:\Users\jwesleylima\LargeFolder', 'rules.json')

# Creating an Organizer
org = Organizer(rm)
org.organize()
```
**Exemplo de saída**

```bash
INFO:root:Starting process in: C:\Users\wlgam\Pictures
INFO:root:Skip unknown extensions: True

WARNING:root:Camera Roll is a directory and has been ignored
WARNING:root:The extension 'ini' was not found on the map
WARNING:root:Images .jfif is a directory and has been ignored
WARNING:root:Images .JPG is a directory and has been ignored
WARNING:root:Saved Pictures is a directory and has been ignored
WARNING:root:Screenshots is a directory and has been ignored
```

## Finalmente
Agora que terminamos as apresentações, fique à vontade para brincar com estas classes sob a licença MIT.
Não esqueça de revisar a licença antes de qualquer coisa.

__(c) 2021 JWesleyLima__
