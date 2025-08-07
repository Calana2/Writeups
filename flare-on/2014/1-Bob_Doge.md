# Bob Doge

Si analizamos el PE en CFF Explorer vemos que llama a `mscoree.dll` y tiene un `IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR` (.NET Directory):

<img width="1024" height="768" alt="photo3" src="https://github.com/user-attachments/assets/280d3480-c693-444b-871f-731166dfa7aa" />

Tambien observamos que hay una cadena cifrada en .rsrc:

<img width="1024" height="768" alt="photo4" src="https://github.com/user-attachments/assets/a61cf2b8-ee08-494c-bf26-f6d46ae60406" />

Usando dnSpy vemos que al hacer click se invoca a `btnDecode_Click`. que toma el secreto y le aplica tres operaciones antes de mostrarlo en el formulario:

<img width="1024" height="768" alt="photo2" src="https://github.com/user-attachments/assets/1d9481b6-23b9-48ff-a033-d93a372acbde" />

Si ponemos un breakpoint despues de la primera operacion podemos ver la cadena descifrada:

<img width="1024" height="768" alt="photo1" src="https://github.com/user-attachments/assets/1a724799-bffb-4515-b2f8-b26eb120e546" />
<br></br>

`3rmahg3rd.b0b.d0ge@flare-on.com`

