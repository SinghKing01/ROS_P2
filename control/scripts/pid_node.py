#!/usr/bin/env python


import rospy
from tf_sim.msg import Float32Stamped

# declaracion de variables globales
desired_val = 0.0
max_integ_error = 0.0
last_error = 0.0
error_acum = 0.0

def exec_pid(error):

  # TODO calcula la sortida del PID fent servir els parametres Kp, Kd, Ki i max_integ_error
  # last_error es el error que obtiene la ultima vez, para calcular la derivada del error
  # error_acum es el error acumulado que se utiliza para para caluclar la parte integral
  # max_integ_error limita el efecto de la parte integral
  global last_error
  global error_acum
  global max_integ_error

  # calculamos la derivada del error
  derivative = error - last_error

  # simplemente sumamos el nuevo error
  error_acum += error

  # si el error_acum es mayor/menor al max_integ_error/-max_integ_err, limitamos con max_integ_error
  if error_acum > max_integ_error:
      error_acum = max_integ_error
  elif error_acum < -max_integ_error:
      error_acum = -max_integ_error

  # caluculamos el salida del controlador PID utilizando la formula
  output = Kp*error + Ki*error_acum + Kd*derivative

  # dado que la salida tiene que estar en %, limitamos si es mayor a 100 o menor a 0
  if output > 100:
      output = 100
  elif output < 0:
      output = 0

  # guardamos el nuevo error en last_error para la proxima iteracion
  last_error = error

  return output

def callbackDesired(input_val):

  global desired_val
  # guardamos en la variable global el valor obtenido
  desired_val = float(input_val.data)


def callbackMeasured(measured_val):

  global desired_val

  # se calcula el error (diferencia entre los valores obtenidos)
  error = desired_val - measured_val.data

  # la salida del controlador PID
  ctrl_val = exec_pid(error)

  # el tiempo actual
  now = rospy.get_rostime()

  # se construye el mensaje tipo Float32Stamped para publicar
  msg = Float32Stamped()
  msg.data = ctrl_val
  msg.header.stamp = now
  pub.publish(msg)

def PID():

  global pub

  global T
  global Kp
  global Kd
  global Ki
  global max_integ_error

  # inicializa el nodo PID
  rospy.init_node('PID')

  # se obtiene la frecuencia como parametro, en caso de que no especifca utiliza 0.0
  freq = rospy.get_param('~frequency', 0.0)
  # obtiene el periodo de muestreo a partir de la frecuencia
  T = 1.0/freq

  # obtiene los parametros Kp, Kd, Ki para calcular PID
  Kp = rospy.get_param('~Kp', 0.0)
  Kd = rospy.get_param('~Kd', 0.0)
  Ki = rospy.get_param('~Ki', 0.0)
  max_integ_term = rospy.get_param('~max_integ_term', 0.0)

  # para limtar los efectos de la parte integral calculamos max_integ_error
  if Ki > 0.0:
    max_integ_error = max_integ_term/Ki

  # se obtiene valores para salida deseada y la que realmente es obtenida
  rospy.Subscriber("~desired_val", Float32Stamped, callbackDesired)
  rospy.Subscriber("~measured_val", Float32Stamped, callbackMeasured)

  # publicamos la salida (output) al topic
  pub = rospy.Publisher('~output', Float32Stamped, queue_size=10)

  rospy.loginfo("PID running")


  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':

  PID()
