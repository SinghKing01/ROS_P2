#!/usr/bin/env python


import rospy
from tf_sim.msg import Float32Stamped

vx3 = 0.0
vx2 = 0.0
vx1 = 0.0
 
vy3 = 0.0
vy2 = 0.0
vy1 = 0.0

vf3 = 0.0
vf2 = 0.0
vf1 = 0.0

def direct_form_I(x_k):

  # TO_DO Implementar el codi a partir de les equacions
  # en diferencies obtingudes amb la forma directa I

  # invocamos las variables globales que contienen últimas tres entradas y salidas
  global vx3
  global vx2
  global vx1

  global vy3
  global vy2
  global vy1

  # guardamos en curx la entrada actual
  curx = x_k

  # actualizamos las variables de entrada introduciendo la nueva entrada
  vx3 = vx2
  vx2 = vx1
  vx1 = curx

  # actualizamos las variables de salida calculando y guardando la nueva salida (vy1)
  vy3 = vy2
  vy2 = vy1
  vy1 = 1.9269*vy2 - 0.9336*vy3 + 0.0665*vx2 - 0.0598*vx3

  return vy1

def direct_form_II(x_k):

  # TO_DO Implementar el codi a partir de les equacions
  # en diferencies obtingudes amb la forma directa II

  # invocamos las variables para los tres f's
  global vf3
  global vf2
  global vf1

  # guardamos en curx la entrada actual
  curx = x_k

  # actualizamos las variables vf's
  vf3 = vf2
  vf2 = vf1
  
  # calculamos y guardamos el nuevo valor para vf1
  vf1 = 0.5*curx + 1.9269*vf2 - 0.9336*vf3

  # caluclamos la salida a partir utilizando la expresion obtenida en direct form II
  cury = 0.1329*vf2 - 0.1196*vf3

  return cury


def callback(input_val):

  # recibe la entrada al sistema y calcula la salida utilizando direct form I y II
  y1 = direct_form_I(input_val.data)
  y2 = direct_form_II(input_val.data)

  # obtiene el tiempo actual y guarda en now
  now = rospy.get_rostime()

  # construye dos mensajes tipo Float32Stamped para publicar topics  
  msg1 = Float32Stamped()
  msg1.data = y1
  msg1.header.stamp = now
  pub1.publish(msg1)

  msg2 = Float32Stamped()
  msg2.data = y2
  msg2.header.stamp = now
  pub2.publish(msg2)

    
def system():

  # se inicializa el node system
  rospy.init_node('system')

  # al recibir la entrada, ejecuta la funcion callback
  rospy.Subscriber("~input", Float32Stamped, callback)

  global pub1
  global pub2

  # publicamos las salidas correspondientes a direct form I y II
  pub1 = rospy.Publisher('output_val_1', Float32Stamped, queue_size=10)
  pub2 = rospy.Publisher('output_val_2', Float32Stamped, queue_size=10)

  # informa que el sistema se esta ejecutando
  rospy.loginfo("System running")


  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':

  system()
