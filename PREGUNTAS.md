## 📋 **Preguntas a responder**
### Ciclo de vida del dato (5b):
- **¿Cómo se gestionan los datos desde su generación hasta su eliminación en tu proyecto?**
  - Los datos proporcionados no los gestiona el Bot, estos datos los gestiona la API de `Football-Data.org`, y mediante funciones de `Python` se hacen las solicitudes necesarias. Es decir, este Bot no guarda ni crea ningún dato, ya que una API los gestiona de manera externa.
- **¿Qué estrategia sigues para garantizar la consistencia e integridad de los datos?**
  - Para asegurar que los datos sean correctos hacemos uso de una API especializada en información y estadísticas sobre fútbol, como es `Football-Data.org`.
- **Si no trabajas con datos, ¿cómo podrías incluir una funcionalidad que los gestione de forma eficiente?**
  - En un futuro, si optáramos por gestionarlos de manera personal sin necesidad de hacer uso de una API hariamos uso de una Base de Datos propia que almacenáse toda la información relacionada a los partidos, calendarios, equipos, estadísticas, etc.

### Almacenamiento en la nube (5f):
- **Si tu software utiliza almacenamiento en la nube, ¿cómo garantizas la seguridad y disponibilidad de los datos?**
  - El bot no utiliza la nube, ya que actualmente se ejecuta de manera local y accede a datos de otro servidor, pero no almacena nada por su cuenta.
- **¿Qué alternativas consideraste para almacenar datos y por qué elegiste tu solución actual?**
  - Para no tener que almacenar datos hemos optado hacer uso de una API como `Football-Data.org`, ya que nos proporciona la comodidad de no tener que actualizar nuestros propios datos.
- **Si no usas la nube, ¿cómo podrías integrarla en futuras versiones?**
  - Una de las opciones que hemos barajado para un futuro si quisiermos utilizar la nube es la personalización para el usuario, como poder guardar sus equipos/competiciones/jugadores favorit@s para que el sistema pueda notificarle sobre estos únicamente, o poder entrar al bot a consultar solo sobre sus intereses.

### Seguridad y regulación (5i):
- **¿Qué medidas de seguridad implementaste para proteger los datos o procesos en tu proyecto?**
  - La seguridad principal ha sido no compartir el `TOKEN` de Telegram ni la `API KEY` de Football-Data.org, sin tener acceso a dichos parámetros el Bot no es ejecutable.
- **¿Qué normativas (e.g., GDPR) podrían afectar el uso de tu software y cómo las has tenido en cuenta?**
  - El Bot cumple con normativas como `GDPR` y `CCPA`, ya que no almacenamos ni procesamos ningún dato personal de los usuarios, así que no afecta en nada al uso del Bot.
- **Si no implementaste medidas de seguridad, ¿qué riesgos potenciales identificas y cómo los abordarías en el futuro?**
  - Como ya se ha comentado, el Bot tiene alguna medida de seguridad, pero en un futuro podriamos mejorarlo con opciones como:
    - Alojar el bot y proteger el código.
    - Controlar el flujo de peticiones para evitar ataques como los DDoS
    - Si se llegaran a utilizar datos de los usuarios, cifrarlos para protegerlos y proporcionar una máxima seguridad.

### Implicación de las THD en negocio y planta (2e):
- **¿Qué impacto tendría tu software en un entorno de negocio o en una planta industrial?**
  - Podría servir para páginas de resultados como BeSoccer que quieran dar el salto a una nueva plataforma, para periodistas de diarios digitales como Marca que quieren estar al tanto de varios partidos a la vez y/o direcciones deportivas de equipos para ojear a los rivales o jugadores para futuros fichajes.
- **¿Cómo crees que tu solución podría mejorar procesos operativos o la toma de decisiones?**
  - Nuestro Bot disminuye los tiempos de búsqueda, ya que desde un mismo lugar puedes preguntar por miles de equipos/jugadores sin tener que navegar entre distintas páginas.
- **Si tu proyecto no aplica directamente a negocio o planta, ¿qué otros entornos podrían beneficiarse?**
  - Simplemente a aficionados del fútbol, sin distinciones, ya que proporcionamos información de varias competiciones.

### Mejoras en IT y OT (2f):
- **¿Cómo puede tu software facilitar la integración entre entornos IT y OT?**
  - El Bot actúa como puente entre IT y OT al tener la recopilación y la distribución de dats de manera automática a través de Telegram, haciendo más fácil la comunicación con la API.
- **¿Qué procesos específicos podrían beneficiarse de tu solución en términos de automatización o eficiencia?**
  - Monitorear los datos en tiempo real.
  - Automatizar las consultas.
  - Centralizar la información.
  - Automatizar notificaciones.
- **Si no aplica a IT u OT, ¿cómo podrías adaptarlo para mejorar procesos tecnológicos concretos?**
  - En el futuro, integrando IA, el bot podría ofrecer respuestas más naturales y personalizadas sin necesidad de comandos. Esto permitiría a directores deportivos, analistas o aficionados consultar información con lenguaje natural, por ejemplo:
      - Q: Oye Bot, dame información sobre Taufek, jugador del Xerez CD.
      - A: Taufek es un veloz y hábil extremo, TOP en su grupo de 2ª RFEF, que en tan solo 2 partidos con el Xerez consiguió dar 2 asistencias y anotar 1 gol.

### Tecnologías Habilitadoras Digitales (2g):
- **¿Qué tecnologías habilitadoras digitales (THD) has utilizado o podrías integrar en tu proyecto?**
  - La API de `Football-Data.org` para toda la información.
  - La API de `TelegramBOT` para poder crear el propio Bot.
- **¿Cómo mejoran estas tecnologías la funcionalidad o el alcance de tu software?**
  - La API de `Football-Data.org` nos proporciona toda la información, lo cual nos ahorra muchísimo trabajo de recopilación de datos.
  - La API de `TelegramBOT` nos da la base sobre la que funcionará el Bot.e