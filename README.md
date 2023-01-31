# File-Organizer-Python v2.0.0
Este projeto tem como propósito entregar uma classe simples que permita, de modo rápido e automatizado, organizar seus arquivos, enviando-os para diretórios personalizados.

## Principais novidades da versão 2.0.0
Todo o código foi reescrito do zero, devido ao novo pensamento
em relação a como o Organizer deve ser escrito e se comportar. Veja abaixo o que mudou:

- Código repensado e reescrito
- Suporte a pathlib
- Uso de glob para encontrar arquivos
- Suporte ao uso de callbacks
- Remoção da classe RulesMap
- Remoção da ideia de _skip_unknown_exts_

### Suporte a glob

Agora é possível utilizar padrões de busca de arquivos para encontrar os arquivos certos de que você precisa. O método [pathlib.Path.glob](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob "Veja como funciona na documentação oficial") é utilizado para esta função. O glob utilizado não é recursivo.

```python
from main import Organizer

target_path = 'C:/Users/you/Downloads'
rules = {
	'*.txt': 'C:/Users/you/Downloads/Text Docs',
	'*.jpg': 'C:/Users/you/Downloads/Images',
	'preffix*': 'C:/Users/you/Downloads/Others'
}

Organizer(target_path, rules).organize()
```

### Suporte ao uso de callbacks
A versão anterior era extremamente limitada à sua bolha de código e não entregava nenhum meio de alto nível para gerenciar a forma como o trabalho era feito. 

Com a adição do suporte a callbacks desta versão, é possível interceptar os arquivos antes que sejam movidos para, por exemplo, cancelar a sua operação ou enviá-los para um lugar personalizado com base em algum critério.

O código a seguir mostra como podemos mover apenas os arquivos que forem maiores do que 5MBs.
```python
from main import Organizer

def five_mb_callback(file):
	expected_size = 5242880 # 5MB in bytes
	curr_file_size = file.stat().st_size
	if curr_file_size >= expected_size:
		return 'C:/Users/you/Downloads/My Files'
	return False

target_path = 'C:/Users/you/Downloads'
rules = { '*': five_mb_callback }
Organizer(target_path, rules).organize()
```

Como podemos ver, para usar uma callback no Organizer, basta adicioná-la como o valor de uma regra específica. Cada arquivo selecionado pelo padrão glob será enviado para essa callback como uma instância de pathlib.Path. Por isso no código acima, é possível utilizar [pathlib.Path.stat()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.stat "Veja como funciona na documentação oficial") para obter o tamanho em bytes do arquivo.

#### Entenda os retornos possíveis
Se uma instância de _str_ ou pathlib.Path forem retornadas, será vista como o caminho de destino do arquivo. Se _False_ for retornado, o arquivo atual será descartado e a iteração continuará.

Se qualquer outra coisa for retornada, será tratada da mesma maneira que _False_, isto é, o arquivo atual será descartado.

## Como fazer outros tipos de operações
Tecnicamente, o Organizer tem uma limitação quanto a operação que é realizada, pois, ao menos por ora, ele apenas _MOVERÁ_ os arquivos. Entretanto, utilizando as _callbacks_, é possível realizar outros tipos de operação, como: _COPIAR_ e _EXCLUIR_.

Para isso, você precisa importar manualmente as dependências de que precisa. Utilizamos, por exemplo, [shutil.copy()](https://docs.python.org/3/library/shutil.html#shutil.copy "Veja como funciona na documentação oficial") para copiar os arquivos.

```python
from main import Organizer
from shutil import copy as copy_file

def copy_file(file):
	file_path = file.absolute()
	dst_path = './copied_files'
	copy_file(file_path, dst_path)
	return False

target_path = './my_files'
rules = { '*': copy_file }
Organizer(target_path, rules).organize()
```

Como pode ser visto, fazemos toda a operação necessária e em seguida retornamos _False_ para que o Organizer descarte o arquivo --- e não o mova mais. Isso funciona para tudo que você queira fazer. Para fazer uma operação de exclusão de um arquivo, pode seguir este mesmo exemplo, porém usando [pathlib.Path.unlink()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.unlink "Veja como funciona na documentação oficial"), por exemplo.

### Como mover apenas diretórios ou apenas arquivos?
Por padrão, o Organizer move qualquer arquivo/diretório que seja selecionado pelo [pathlib.Path.glob](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob "Veja como funciona na documentação oficial"). Em algumas situações pode ser desejável operar apenas com os arquivos ou apenas com os diretórios. Novamente, podemos utilizar as _callbacks_ para fazer isso.

#### Mover apenas arquivos
```python
...
def only_files(file):
	if not file.is_file():
		return False
	return './destination'
...
```

_Essa função moverá apenas os arquivos._<br>
O mesmo pode ser feito para diretórios, porém usando [pathlib.Path.is_dir()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_dir "Veja como funciona na documentação oficial") ao invés de [pathlib.Path.is_file()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_file "Veja como funciona na documentação oficial").

## Desempenho
Esta nova versão está buscando ser muito mais otimizada do que a anterior. Não só em relação à forma como o código é escrito, mas também na flexibilidade e versatilidade de personalização na hora de utilizar e no desempenho.

Dando foco especial para o desempenho, há algumas mudanças consideráveis. Fiz um teste de qualidade para comparar a funcionalidade e velocidade da versão anterior e da nova. Como o modelo de uso das duas classes é um pouco diferente, tentou-se simular o mesmo uso. Veja como funcionou:

### Teste de velocidade
O teste foi mover os seguintes arquivos, cada um para o seu diretório personalizado. Arquivos _mp3_ deveriam ser enviados para um diretório _Músicas_, por exemplo.
```
file_0.mp3 - 689106 bytes (0.66MB)
file_1.mp3 - 3985660 bytes (3.80MB)
file_2.mp3 - 3249348 bytes (3.10MB)
file_3.mp3 - 6882800 bytes (6.56MB)
file_4.mp3 - 2853023 bytes (2.72MB)
file_5.mp3 - 4056211 bytes (3.87MB)
file_6.mp3 - 1876022 bytes (1.79MB)
file_7.mp3 - 4665707 bytes (4.45MB)
file_8.py - 4675 bytes
file_10.txt - 1176 bytes
```

### Resultados
- **Versão anterior**
	Levou 0.29seg para terminar o teste
- **Versão nova**
	Levou 0.07seg para terminar o mesmo teste
	GANHO DE +75.8% de velocidade

### Explicação do aumento de desempenho
O considerável aumento de desempenho se dá pelo uso de padrões glob, pois são selecionados apenas os arquivos que importam para a operação, enquanto a versão anterior percorre todos os arquivos --- um por um -- em busca de uma correspondência para assim mover o arquivo.