# Cube-Visualization

A python based application to visualize how various sensor fusion algorithms work. It receives data transmitted by the [AndyIMU][1] android application, performs a user specified sensor fusion algorithm, and rotates a 3-D cube to help the user visualize their output.

#### Required modules
1. [Tkinter][2]: For the GUI
	```
	pip install tk
	```
2. [PyOpenGL][3]: For rendering 3D graphics
	```
	pip install PyOpenGL PyOpenGL_accelerate
	```
3. [PyGame][4]: Container for 3D graphics
	```
	pip install pygame
	```
	
#### Demo
![demo-gif](some-gif)

> Note: The ReferenceCodes folder contains code that implements various functionalities of the application independently.

### Adding custom sensor fusion algorithm
1. Open the file **d_sensorFusion.py**
2. Add a method, for example, **fusionAlgo** to the class *Fusion*
3. You can obtain the raw data from sensor as a 1x6 array (accelerometer values followed by gyroscope values) or 1x9 array (accelerometer, gyroscope followed by magnetometer) by using the `get()` method of `self.rawData` queue.
4. The size of array depends whether the android application is transmitting magentometer values or not.
5. Before storing the result into final variables, add statement `Rpy.lock.acquire()` to lock the variables to the current thread so that the visualizing section does not read the values.
6. Store the final result of your algorithm in variables 
	- *Rpy.rotateX*: Rotation about X axis 
	- *Rpy.rotateY*: Rotation about Y axis
	- *Rpy.rotateZ*: Rotation about Z axis
7. End your function using
```
try:
	Rpy.lock.notify()
finally:
	Rpy.lock.release()
```
8. Call your function in the `run` method

#### Sample function
```
def fusionAlgo:
	raw_values = self.rawData.get()
	...
	... # algorithm on raw_values
	...
	
	Rpy.lock.acquire()
	Rpy.rotateX = some_value
	Rpy.rotateY = another_value
	Rpy.rotateZ = yet_another_value
	
	try:
		Rpy.lock.notify()
	finally:
		Rpy.lock.release()
```


[1]:link-andyIMU-repo
[2]:https://wiki.python.org/moin/TkInter
[3]:https://wiki.python.org/moin/PyOpenGL
[4]:https://pypi.org/project/pygame/