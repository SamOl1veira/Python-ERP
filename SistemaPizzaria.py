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

def cadastrarPedido():
    listarProduto()
    idPedido = input("Digite o id do produto pedido\n")
    localEntrega=input("Digite o local de entrega do pedido\n")
    observacoesPedido=input("Digite as observações do pedido\n")
    try:
        with conexao.cursor() as cursor:
            cursor.execute("select nome from produtos where id={}".format(idPedido))
            nomePedido=cursor.fetchone()
            nome=nomePedido['nome']

            cursor.execute("select ingredientes from produtos where id={}".format(idPedido))
            ingredientesPedido=cursor.fetchone()
            ingredientes=ingredientesPedido['ingredientes']

            cursor.execute("select grupo from produtos where id={}".format(idPedido))
            grupoPedido=cursor.fetchone()
            grupo=grupoPedido['grupo']

    except:
        print("erro ao pegar as variaveis do pedido.")
    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into pedidos '
                           '(nome, ingredientes, grupo, localEntrega, observacoes)'
                           'values (%s,%s,%s,%s,%s)',
                           (nome,
                            ingredientes, grupo,localEntrega,observacoesPedido))
            conexao.commit()
            print("Pedido cadastrado com sucesso!")
    except:
        print("Não foi possivel inserir o pedido no banco de dados")

def listarProduto():
    produtos=[]

    try:
        with conexao.cursor() as cursor:
            cursor.execute("select * from produtos")
            produtosCadastrados=cursor.fetchall()

    except:
        print("Erro ao fazer consulta no banco de dados")

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos)!=0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print("Produto não encontrado")

def excluirProduto():
    idDeletar=int(input("digite o id do produto a ser apagado\n"))
    try:
        with conexao.cursor() as cursor:
            cursor.execute("delete from produtos where id = {}".format(idDeletar))

    except:
        print("erro ao excluir produto")

def listarPedidos():
    pedidos=[]
    decisao=0
    while decisao!=2:
        pedidos.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute("select * from pedidos")
                listaPedidos=cursor.fetchall()
        except:
            print("erro no banco de dados\n")

        for i in listaPedidos:
            pedidos.append(i)
        if len(pedidos)!=0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print("nenhum pedido encontrado")
        decisao=int(input("digite 1 para das um pedido como entregue e 2 para voltar\n"))

        if decisao == 1:
            idPedir=int(input("digite o id do pedido entregue\n"))
            try:
                with conexao.cursor() as cursor:
                    cursor.execute("delete from pedidos where id = {}".format(idPedir))
                    print("pedido entregue!")
            except:
                print("erro ao acessar o banco de dados\n")

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
            decisaousuario=int(input("digite 0 para sair, 1 para cadastrar produtos, \n"
                                     "2 para listar produtos, 3 para listar os pedidos, 4 para fazer um pedido\n"))
            if decisaousuario==1:
                cadastrarProdutos()
            elif decisaousuario==2:
                listarProduto()
                delete=int(input("digite 1 para excluir um produto e 2 para sair"))
                if delete==1:
                    excluirProduto()
            elif decisaousuario==3:
                listarPedidos()
            elif decisaousuario==4:
                cadastrarPedido()
