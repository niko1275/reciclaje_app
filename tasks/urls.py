
from django.urls import path
from  . import views


urlpatterns = [
   
    path('registro',views.registro,name='registro'),
    path('login',views.login,name='login'),
    path('cerrar_sesion',views.cerrar_sesion,name='cerrar_sesion'),
    path('preguntas',views.preguntas,name='preguntas'),
    path('Beneficios',views.Beneficios,name='Beneficios'),
    path('calculadora',views.calculadora,name='calculadora'),
    path('Ubicaciones',views.Ubicaciones,name='Ubicaciones'),
    path('informativo',views.informativo,name='informativo'),
    path('somos',views.somos,name='somos'),
    path('',views.index,name='index'),
    path('comentarios,<str:id>',views.comentarios,name='comentarios'),
    path('UsuarioEdit',views.UsuarioEdit,name='UsuarioEdit'),
    path('Usuario',views.Usuario,name='Usuario'),
    path('borrarComentario<str:id>',views.borrarComentario,name='borrarComentario'),
    path('borrarComentarioUser/<str:id>/<str:id2>/',views.borrarComentarioUser,name='borrarComentarioUser'),
    path('editarPregunta<str:id>',views.editarPregunta,name='editarPregunta'),
    path('editarComentario/<str:id>/<str:id2>/',views.editarComentario,name='editarComentario'),
     path('reaccionar/<str:id>/', views.reaccionar, name='reaccionar'),
]

