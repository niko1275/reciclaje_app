from django.shortcuts import render,redirect
from django.contrib import sessions
import pyrebase
# Create your views here.


firebaseConfig = {
  "apiKey": "AIzaSyDptkEBCsXjtSqBHgfhxghoKGJ0Vo26vCU",
  "authDomain": "reciclaje-fee09.firebaseapp.com",
  "databaseURL": "https://reciclaje-fee09-default-rtdb.firebaseio.com",
  "projectId": "reciclaje-fee09",
  "storageBucket": "reciclaje-fee09.appspot.com",
  "messagingSenderId": "619994282425",
  "appId": "1:619994282425:web:ff66f7598ec7e9d6145e68",
  "measurementId": "G-PP8J8QTJRS"
}


firebase= pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database=firebase.database()


storage = firebase.storage()

# local_file_path = "C:/Users/nikoc/Desktop/Django/Reciclaje/static/fotos/casaa.png"
# destination_path = "gs://reciclaje-fee09.appspot.com/img/casaa.png"

# storage.child(destination_path).put(local_file_path)

def index(request):
    useractivo=user_id = request.session.get('user_id')

    if useractivo:
        user=database.child('usuarios').child(user_id).get().val()
        return render(request,'index.html',{'user':user})
    else:
        return render(request,'index.html')

def login(request):
 
  if request.method=='POST':
        email = request.POST['email']
        password= request.POST['contraseña']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']
            request.session['user_id'] = user_id
            print("Inicio de sesión exitoso")
            print("Token de acceso:", user['idToken'])
            
        
        except Exception as e:
            print("Error al iniciar sesión:", str(e))
            context = {'error':'Error al iniciar sesión, Email o contraseña erroneos, intente nuevamente'}
            return render(request,'login.html',context)
    
       
  return render(request,'login.html')



def cerrar_sesion(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    
    # Redirigir a la página de inicio o a otra página deseada
        return redirect('index')




def registro(request):
    if request.method=='POST':
        try:
            email = request.POST['email']
            password= request.POST['contraseña']
            nombre=request.POST['nombre']

            if email and password:
                user = auth.create_user_with_email_and_password(email, password)
                user_id = user["localId"]
                db = firebase.database()
                data = {
                "nombre": nombre,
                "email": email
                }
                db.child("usuarios").child(user_id).set(data)
                return redirect('index')
        except:
            context = {'error':'Error al registrarse, intente nuevamente'}
            return render(request, 'registro.html', context)
    return render(request,'registro.html')

def reaccionar(request, id):
    user_id = request.session.get('user_id')

    reaccion_actual = database.child("preguntas").child(id).child("reacciones").child(user_id).get().val()

    if reaccion_actual is not None:
        database.child("preguntas").child(id).child("reacciones").child(user_id).set(None)
    else:
        database.child("preguntas").child(id).child("reacciones").child(user_id).set(True)
    return redirect('preguntas')



def preguntas(request):
    print("Llego")
    user_id = request.session.get('user_id')
    print(user_id)
    if request.method == 'POST':
        
        pregunta = request.POST.get('pregunta')
        descripcion = request.POST.get('descripcion')
        
        usuario = database.child('usuarios').child(user_id).child('nombre').get().val()
        comentarios = database.child("usuarios").child(user_id).child("comentarios")
        
        if comentarios:
            numero_comentarios = len(comentarios.keys())
            print(f"El número de comentarios es: {numero_comentarios}")
        else:
            print("El usuario no tiene comentarios.")
        if pregunta and descripcion:
            user_id = request.session.get('user_id')
            
            database.child('preguntas').push({
                'titulo': pregunta,
                'descripcion': descripcion,
                'autor': user_id,
                'usuario':usuario,
            })

            return redirect('preguntas')  
    
    user_id = request.session.get('user_id')
    preguntas = database.child('preguntas').get().val()
   
    return render(request, 'preguntas.html', {
        'preguntas': preguntas,
        'user_id':user_id,
    })





def comentarios(request, id):
    
    documento = database.child("preguntas").child(id).get().val()
    

    # comentario_ref = database.child("preguntas").child(id).child("comentarios").child(comentario_id)
    if request.method == 'POST':
        comentarioUser = request.POST.get('comentario')
        user_id = request.session.get('user_id')
        usuario = database.child('usuarios').child(user_id).child('nombre').get().val()
    
        if comentarioUser:
            comentario_data = {
                'contenido': comentarioUser,
                'autor': user_id,
                'usuario': usuario
            }


            database.child("preguntas").child(id).child("comentarios").push(comentario_data)

            return redirect('comentarios', id=id)
        
    comentarios_ref = database.child("preguntas").child(id).child("comentarios").get().val() 
    user_id = request.session.get('user_id')
    
    return render(request, 'comentarios.html', {
        'documento': documento,
        'comentarios_ref': comentarios_ref,
        'user_id':user_id,
        'id':id
       
    })




def Beneficios(request):
    return render(request,'Beneficios.html')


def calculadora(request):

    if request.method == 'POST':
        # personas = request.POST.get('personas')
        
        electricidad = request.POST.get('consumo')
        if electricidad == '':
            electricidad = 0
        else:
            electricidad = float(request.POST.get('consumo'))
        
        transporte = request.POST.get('transporte')
        if transporte == '':
            transporte = 0
        else:
            transporte = float(request.POST.get('transporte'))
        
        gas = request.POST.get('gas')
        if gas == '':
            gas = 0
        else:
            gas = float(request.POST.get('gas'))
        
        relectricidad = ((electricidad/118)*0.233)*12
        rtransporte = (transporte*2.3)*12
        rgas = (gas*1.3)*12
        resultado = relectricidad + rtransporte + rgas
        resultado = round(resultado, 3)
        context = {'resultado':'Emision de '+str(resultado)+'Kg de CO2 por año'}

        user_id = request.session.get('user_id')

        existing_data = database.child("calculadora").order_by_child("usuario").equal_to(user_id).get().val()
        
        if existing_data:
            message = "Has calculado tu huella de carbono. Puedes ver los resultados en tus opciones de usuario."

            return render(request, 'calculadora.html' , {
                'message':message
            })
      
        data = {
            'resultado': resultado,
            'usuario': user_id
        }
        database.child("calculadora").push(data)
        context = {'resultado': 'Emision de '+str(resultado)+'Kg de CO2 por año'}

        return render(request,'calculadora.html',context)
    
    return render(request,'calculadora.html')



def informativo(request):
    return render(request,'informativo.html')


def Ubicaciones(request):
    return render(request,'Ubicaciones.html')

def somos(request):
    return render(request,'somos.html')

def my_view(request):
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley/video.mp4"
    return render(request, 'informativo.html', {'video_url': video_url})


def UsuarioEdit(request):
    return render(request,'UsuarioEdit.html')


def Usuario(request):
    user_id = request.session.get('user_id')
    usuario = database.child('usuarios').child(user_id).get().val()
    print(user_id)

    try:
        calculadora_data = database.child("calculadora").order_by_child("usuario").equal_to(user_id).get().val()
        usuario = database.child('usuarios').child(user_id).get().val()
        if not calculadora_data:
            message = 'No has utilizado la calculadora'
            return render(request, 'Usuario.html', {'message': message, 'usuario': usuario})

    except:
        message = 'No se encontró información del usuario'
        return render(request, 'Usuario.html', {'message': message})
    
    usuario = database.child('usuarios').child(user_id).get().val()
    return render(request, 'Usuario.html', {'calculadora_data': calculadora_data, 'usuario': usuario})




def borrarComentario(request, id):
    pregunta_ref = database.child("preguntas").child(id)

    pregunta_ref.remove()
    return redirect('preguntas')


 
def borrarComentarioUser(request,id,id2):
    print(id)
    print(id2)
    pregunta_ref = database.child("preguntas").child(id).child('comentarios').child(id2)
    pregunta_ref.remove()
    return redirect('comentarios' ,id=id)


def editarPregunta(request,id):
    print(id)
    preguntas = database.child("preguntas").child(id).get().val
    if request.method=='POST':
        titulo =request.POST['titulo']
        descripcion=request.POST['descripcion']
        
        if titulo and descripcion:
            data={
                'titulo':titulo,
                'descripcion':descripcion,
            }
            database.child("preguntas").child(id).update(data)

            return redirect('preguntas')
        
    return render(request,'editarPregunta.html',{
        'preguntas':preguntas,
    })


def editarComentario(request,id,id2):
    comentario= database.child("preguntas").child(id).child('comentarios').child(id2).get().val()


    if request.method=='POST':
        descripcion=request.POST['contenido']
        if descripcion:
            data={
                'contenido':descripcion
            }
            comentario= database.child("preguntas").child(id).child('comentarios').child(id2).update(data)
            return redirect('comentarios', id=id )
    return render(request,'editarComentario.html',{'comentario':comentario})