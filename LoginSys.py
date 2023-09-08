import pymysql.cursors

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def logCasdastro():
    #Função para automação do uso de login e cadastro
    """Aqui todos os cadastros feitos serão aceitos
          Mas entende-se aqui que poderia haver a nescessidade
          de aprovar um cadastro pelo administrador.
          Também deve-se observar a ausencia da plena complexidade
          que um sistema de login e cadastro exigiria, isto se deve
          por se tratar de um sistema teste, demonstrativo."""
    usuarioExistente = 0
    autenticado=False
    usuarioMestre=False

    if decisao==1:
        nome=input("digite seu nome ")
        senha=input("digite sua senha ")

        for l in resultado:
            if nome == l['nome'] and senha == l['senha']:
                if l['nivel']==1:
                    usuarioMestre=False
                elif l['nivel']==2:
                    usuarioMestre=True
                autenticado=True
                break
            else:
                autenticado=False
        if not autenticado:
            print("Email ou senha errados")
    elif decisao==2:
        print('Faça seu cadastro')
        nome=input('digite seu nome: \n')
        senha=input("digite sua senha: \n")

        for l in resultado:
            if nome == l['nome'] and senha == l['senha']:
                usuarioExistente=1

        if usuarioExistente==1:
            print("Usuário já existe ")
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome, senha, nivel)'
                                   'values (%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                print("Usuário cadastrado com sucesso!")
            except:
                print("Erro ao inserir os dados no banco.")
    return autenticado, usuarioMestre

def cadastrarProdutos():
    nome=input("Digite o nome do produto\n")
    ingredientes=input("Digite os ingredientes do produto\n")
    grupo=input("Digite a que grupo pertecen este produto\n")
    preco=float(input("Digite o preço do produto\n"))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos '
                           '(nome, ingredientes, grupo, preco)'
                           'values (%s,%s,%s,%s)',
                           (nome, ingredientes, grupo, preco))
            conexao.commit()
            print("Produto cadastrado com sucesso!")
    except:
        print("Não foi possivel inserir o produto no banco de dados")


autentico=False
while not autentico:
    decisao=int(input("digite 1 para logar e 2 para cadastrar \n"))

    try:
        with conexao.cursor() as cursor:
            cursor.execute("select * from cadastros")
            resultado=cursor.fetchall()

    except:
        print("Erro ao conectar no banco de dados")

    autentico, usuarioSupremo = logCasdastro()

if autentico:
    print("\nAutenticado!\n")
    if usuarioSupremo == True:
        decisaousuario=1
        while decisaousuario!=0:
            decisaousuario=int(input("digite 0 para sair, 1 para cadastrar produtos\n"))
            if decisaousuario==1:
                cadastrarProdutos()
