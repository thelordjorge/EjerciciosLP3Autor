from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Articulo
from miapp.models import Autor
from django.db.models import Q

# Create your views here.
layout = """
    <h1> Proyecto Web (LP3) || Marco Amasifuen </h1>
    <hr/>
    <ul>
        <li>
            <a href="/inicio">Inicio</a>
        </li>
        <li>
            <a href="/saludo">Mensaje de Saludo</a>
        </li>
        <li>
            <a href="/rango">Mostrar Numeros [a,b]</a>
        </li>
        <li>
            <a href="/rango2">Mostrar Numeros [a,b] (Con Parámetro)</a>
        </li>
    </ul>
    <hr/>
"""


def index(request):
    estudiantes = [
        'SERGIO DANIEL VITE COCHACHIN',
        'ANTHONY GERARDO BENDEZU SANTISTEBAN',
        'CRISTIAN ALEXIS CHIPANA HUAMAN',
        'CARLOS GUSTAVO OYOLA SAAVEDRA',
        'GERARDO MANUEL CASTILLO TORDOYA'
    ]
    
    return render(request, 'index.html', {
        'titulo': 'Inicio',
        'mensaje': 'Proyecto Web con DJango',
        'estudiantes': estudiantes
    })


def saludo(request):
    return render(request, 'saludo.html', {
        'titulo': 'Saludo',
        'autor_saludo': 'Marco Antonio Amasifuen Rivera'
    })


def rango(request):
    a = 10
    b = 20
    rango_numeros = range(a,b+1)
    return render(request, 'rango.html',{
        'titulo': 'Rango',
        'a':a,
        'b':b,
        'rango_numeros':rango_numeros
    })


def rango2(request, a=0, b=100):
    if a > b:
        return redirect('rango2', a=b, b=a)

    resultado = f"""
        <h2> Rango con parámetros </h2>
        <h2> Número de [{a},{b}] </h2>
        Resultado: <br>
        <ul>
    """
    while a <= b:
        resultado += f"<li> {a} </li>"
        a += 1

    resultado += "</ul>"
    return HttpResponse(layout + resultado)

def crear_articulo(request, titulo, contenido, publicado):
    articulo = Articulo(
        titulo = titulo,
        contenido = contenido,
        publicado = publicado
    )

    articulo.save()
    return HttpResponse(f"Articulo Creado: {articulo.titulo} - {articulo.contenido}")

def buscar_articulo(request, number):
    try:
        articulo = Articulo.objects.get(id=number)
        resultado = f"""Articulo: 
                        <br><strong>ID: </strong> {articulo.id}
                        <br><strong>Titulo: </strong> {articulo.titulo}
                        <br><strong>Contenido: </strong>{articulo.contenido}
                        """
    except:
        resultado = "<h1>Articulo No Encontrado </h1>"
    return HttpResponse(resultado)

def editar_articulo(request, id):
    articulo = Articulo.objects.get(pk = id)

    articulo.titulo = "Enseñanza online en la UNTELS"
    articulo.contenido = "Aula Virtual, Google Meet, Portal Académico ..."
    articulo.publicado = False

    articulo.save()
    return HttpResponse(f"Articulo Editado: {articulo.titulo} - {articulo.contenido}")

def listar_articulos(request):
    articulos =  Articulo.objects.order_by('titulo').filter(id__lt = 6)
    return render(request, 'listar_articulos.html',{
    'articulos' : articulos,
    'titulo' : 'Listado de Artículos'
    })

def eliminar_articulo(request, id):
    articulo = Articulo.objects.get(pk = id)
    articulo.delete()
    return redirect('listar_articulos')

def save_articulo(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        if len(titulo)<=5:
            return HttpResponse("<h2>El tamaño del título es pequeño, intente nuevamente</h2>")
        contenido = request.POST['contenido']
        publicado = request.POST['publicado']

        articulo = Articulo(
            titulo = titulo,
            contenido = contenido,
            publicado = publicado
        )
        articulo.save()
        return HttpResponse(f"Articulo Creado: {articulo.titulo} - {articulo.contenido}")
    else:
        return HttpResponse("<h2> No se ha podido registrar el artículo </h2>")

def crear_autor(request, nombre, apellido, sexo, fecha, pais):
    autor = Autor(
        nombre = nombre,
        apellido = apellido,
        sexo = sexo,
        fecha = fecha,
        pais = pais
    )
    autor.save()
    return HttpResponse(f"Autor Creado: {autor.nombre} - {autor.apellido} - {autor.sexo} - {autor.fecha} - {autor.pais} ")

def save_autor(request):
    if (request.method == 'POST'):
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        sexo = request.POST['sexo']
        fecha = request.POST['fecha']
        pais = request.POST['pais']
        """ if len(titulo)<=5:
                return HttpResponse("<h2>El tamaño del título es pequeño, intente nuevamente</h2>") """
            
        autor = Autor(
            nombre = nombre,
            apellido = apellido,
            sexo = sexo,
            fecha = fecha,
            pais = pais
        )
        autor.save()
        return HttpResponse(f"Autor Creado: {autor.nombre} - {autor.apellido} - {autor.sexo} - {autor.fecha} - {autor.pais}")
    else:
        return HttpResponse("<h2> No se ha podido registrar el autor </h2>")

def create_autor(request):
    return render(request, 'create_autor.html')

def listar_autores(request):
    autores =  Autor.objects.all()
    return render(request, 'listar_autores.html',{
    'autores' : autores,
    'titulo' : 'Listado de Autores'
    })

def eliminar_autor(request, id):
    autor = Autor.objects.get(pk = id)
    autor.delete()
    return redirect('listar_autores')



