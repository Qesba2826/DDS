from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager, UserMixin
from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'productosdb'

mysql = MySQL(app)
app.secret_key='mysecretkey'

#INICIO
@app.route("/")
def loggin():
    return render_template('login.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/reg")
def reg():
    return render_template('registered.html')

@app.route("/regcli")
def cuenta():
    cur = mysql.connection.cursor()
    cur.execute("select * from cliente")
    data = cur.fetchall()
    return render_template("cuenta.html", cliente=data)

@app.route("/regven")
def cuenta():
    cur = mysql.connection.cursor()
    cur.execute("select * from vendedor")
    data = cur.fetchall()
    return render_template("cuenta.html", vendedor=data)

@app.route("/productos")
def cuenta():
    cur = mysql.connection.cursor()
    cur.execute("select * from productos")
    data = cur.fetchall()
    return render_template("products.html", producto=data)

@app.route("/checkout")
def cuenta():
    cur = mysql.connection.cursor()
    cur.execute("select * from lista")
    data = cur.fetchall()
    return render_template("checkout.html", lista=data)


@app.route("/add_registro_cliente", methods=["POST"])
def add_registro_cliente():
        if request.method == "POST":
            nom = request.form["nombres"]
            dis = request.form["distrito"]
            direc = request.form["direccion"]
            em = request.form["email"]
            cel = request.form["telefono"]
            contra = request.form["contrasena"]
            
            cur2 = mysql.connection.cursor()
            cur2.execute("select email from cliente")
            clientes = cur2.fetchall()

            em_cliente=None
            
            #print(str(users))
            #for email in users :
             #   if (email[0] == em):
              #      print("correo existe")
               #     return "El correo ya existe"
            
            for email in clientes :
                if (email[0] == em):
                    em_cliente = email[0]

            if em_cliente == em:
                print("elige otro correo")             
                return redirect(url_for("regcli"))

            print("INSERT", id, nom, dis, direc, em, cel, contra)
            cur = mysql.connection.cursor()
            cur.execute("insert into cliente(nombres, distrito, direccion, email, telefono, contrasena) values(%s,%s,%s,%s,%s,%s)", (nom, dis, direc, em, cel, contra))
            mysql.connection.commit()
            flash("Registro como cliente exitoso")
            return redirect(url_for('index'))
        return render_template ("index.html")

@app.route("/add_registro_vendedor", methods=["POST"])
def add_registro_vendedor():
        if request.method == "POST":
            nom = request.form["nombres"]
            ruc = request.form['RUC']
            dis = request.form["distrito"]
            direc = request.form["direccion"]
            em = request.form["email"]
            cel = request.form["telefono"]
            contra = request.form["contrasena"]
            
            cur2 = mysql.connection.cursor()
            cur2.execute("select email from vendedor")
            clientes = cur2.fetchall()

            em_cliente=None

            for email in clientes :
                if (email[0] == em):
                    em_cliente = email[0]

            if em_cliente == em:
                print("elige otro correo")             
                return redirect(url_for("regven"))

            print("INSERT", id, nom, dis, direc, em, cel, contra)
            cur = mysql.connection.cursor()
            cur.execute("insert into vendedor(nombres, RUC, distrito, direccion, email, telefono, contrasena) values(%s,%s,%s,%s,%s,%s,%s)", (nom, ruc, dis, direc, em, cel, contra))
            mysql.connection.commit()
            flash("Registro como cliente exitoso")
            return redirect(url_for('index'))
        return render_template ("index.html")


@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    if request.method == 'POST':
        nom = request.form['nombre']
        can = request.form['cantidad']
        mar = request.form['marca']
        tam = request.form['tamano']
        print('UPDATE', id, nom, can, mar, tam)
        cur= mysql.connection.cursor()
        cur.execute('insert into lista(producto, cantidad, marca, tamano) values(%s, %s, %s, %s)', (nom, can, mar, tam))
        mysql.connection.commit()
        flash('Producto insertado correctamente')
        return redirect(url_for('carrito'))
    
@app.route('/edit/<id>')
def edit_pedido(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from lista where id = %s', {id})
    data = cur.fetchall()
    print(data[0])    
    return render_template('edit.html', lista=data[0])

@app.route('/delete/<string:id>')
def delete_pedido(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from lista where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('carrito'))

@app.route('/limpiar/')
def limpiar_pedido():
    cur = mysql.connection.cursor()
    cur.execute('delete from lista')
    mysql.connection.commit()
    flash('Todos los productos de la lista han sido eliminados')
    return redirect(url_for('carrito'))

@app.route('/envio/')
def envio_contact():
    cur = mysql.connection.cursor()
    cur.execute('select * from lista')
    data = cur.fetchall()
    
    return render_template('envio.html', lista=data)
    flash('Su lista de productos ha sido enviada a las tiendas más cercanas. Pronto recibirá la aceptación de su pedido.')
    
@app.route('/update/<id>',methods=['POST'])
def update_contact(id):

    if request.method == 'POST':
        nom = request.form['nombre']
        can = request.form['cantidad']
        mar = request.form['marca']
        tam = request.form['tamano']
        print('UPDATE', id, nom, can, mar, tam)
        cur = mysql.connection.cursor()
        cur.execute("""
            update lista
            set nombre = %s,
            cantidad = %s,
            marca = %s,
            tamano = %s
            where id = %s
        """, (nom, can, mar, tam, id) )
        mysql.connection.commit()
        flash('Lista de productos actualizada correctamente')
        return redirect(url_for('carrito'))

#VENDEDOR
@app.route('/vendedor_index')
def vendedor_index():
    cur = mysql.connection.cursor()
    cur.execute('select *from productos')
    data =cur.fetchall()
    return render_template('index.html', producto=data)
    #return 'Index - DS'

@app.route('/venta')
def venta():
    cur = mysql.connection.cursor()
    cur.execute('select *from lista')
    data =cur.fetchall()
    return render_template('venta.html', lista=data)

@app.route('/add_lista', methods=['POST'])
def add_lista():
    if request.method == 'POST':
        chk = request.form['ck']

        print('INSERT', id, chk)
        cur = mysql.connection.cursor()
        cur.execute('insert into lista(ck) values(%s)', (chk))
        mysql.connection.commit()
        flash('Producto checkeado correctamente')
        return redirect(url_for('venta'))

@app.route('/add_product',methods=['POST'])
def add_product():
    if request.method == 'POST':
        cod = request.form['id']
        nom = request.form['nombre']
        stk = request.form['stock']
        mar = request.form['marca']
        tam = request.form['tamano']
        pre = request.form['precio']

        print('INSERT', id, nom, stk, mar, tam, pre)
        cur = mysql.connection.cursor()
        cur.execute('insert into productos(id,nombre,stock,marca,tamano,precio) values(%s,%s,%s,%s,%s,%s)', (cod, nom, stk, mar, tam, pre))
        mysql.connection.commit()
        flash('Producto Insertado correctamente')
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from productos where id = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', producto=data[0])

@app.route('/editstock/<id>')
def edit_stockproduct(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from productos where id = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('editstock.html', producto=data[0])

@app.route('/delete/<string:id>')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from productos where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto Eliminado correctamente')
    return redirect(url_for('index'))

@app.route('/update/<id>',methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        cod = request.form['id']
        nom = request.form['nombre']
        stk = request.form['stock']
        mar = request.form['marca']
        tam = request.form['tamano']
        pre = request.form['precio']
        print('UPDATE', cod, nom, stk, mar, tam, pre)
        cur = mysql.connection.cursor()
        cur.execute("""
            update productos
            set id = %s,
                nombre = %s,
                stock = %s,
                marca = %s,
                tamano = %s,
                precio = %s
            where id = %s
        """,(cod, nom, stk, mar, tam, pre, id) )
        mysql.connection.commit()
        flash('Producto actualizado correctamente')
        return redirect(url_for('index'))

@app.route('/updatestock/<id>',methods=['POST'])
def update_stockproduct(id):
    if request.method == 'POST':
        stk = request.form['stock']
        print('UPDATE',stk)
        cur = mysql.connection.cursor()
        cur.execute("""
            update productos
            set stock = %s
            where id = %s
        """,(stk, id) )
        mysql.connection.commit()
        flash('Stock actualizado correctamente')
        return redirect(url_for('index'))

@app.route('/updatev/<id>',methods=['POST'])
def update_venta(id):

    if request.method == 'POST':
        chk = request.form['ck']
        print('UPDATE',chk)
        cur = mysql.connection.cursor()
        cur.execute("""
            update lista
            set ck = %s
            where id =%s
        """,(chk, id) )
        mysql.connection.commit()
        flash('Producto actualizado')
        return redirect(url_for('venta'))

@app.route('/total',methods=['GET', 'POST'])
def totales(p1, c1):
    try:
        p1 = request.form['precio']
        c1 = request.form['cantidad']

        t0=0

        t0=t0+p1*c1
        return render_template("venta.html", t0)

if __name__ == '__main__':
    app.run(port=3000, debug=True)