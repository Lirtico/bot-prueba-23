# 🐨 Koala Bot

Un bot de Discord multifuncional y modular con características avanzadas de moderación, interacciones divertidas y utilidades para servidores.

## ✨ Características

### 🤖 Características Principales
- **Arquitectura Modular** - Organizado en cogs separados para fácil mantenimiento
- **Comandos de Moderación** - Sistema completo de moderación con cárcel y advertencias
- **Interacciones con GIFs** - Más de 50 comandos de interacciones con GIFs anime
- **Comandos de Diversión** - Entretenimiento con dados, chistes, memes y más
- **Utilidades Avanzadas** - Información de usuarios, servidores, clima, traductor
- **Sistema de Logging** - Registro detallado de eventos y actividades
- **Soporte Multi-idioma** - Comandos en español

### 🛡️ Moderación y Seguridad
- **Sistema de Cárcel** - Aislamiento temporal de usuarios problemáticos
- **Sistema de Advertencias** - Disciplina progresiva para violaciones
- **Detección de Amenazas** - Análisis en tiempo real de spam y raids
- **Filtrado de Mensajes** - Eliminación automática de enlaces maliciosos
- **Gestión de Roles** - Asignación y gestión avanzada de roles

### 🎭 Interacciones y Diversión
- **50+ Comandos de Interacción** - Hug, slap, kiss, pat, tickle, y muchos más
- **Comandos de Anime** - Todos los comandos incluyen GIFs de anime
- **Comandos Divertidos** - Dados, chistes, memes, 8-ball, calculadora
- **Comandos de Comunidad** - Encuestas, recordatorios, clima, traductor

### 📊 Información y Utilidades
- **Información de Usuarios** - Avatar, banner, información detallada
- **Información de Servidor** - Estadísticas completas del servidor
- **Información de Canales** - Detalles de canales y permisos
- **Información de Roles** - Información detallada de roles

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- Token de Bot de Discord (de [Discord Developer Portal](https://discord.com/developers/applications))

### Configuración
1. **Clona o descarga** los archivos del bot

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura el bot**:
   - Edita `main.py` y reemplaza `"YOUR_BOT_TOKEN_HERE"` con tu token real
   - O usa variables de entorno: `export DISCORD_TOKEN=tu_token_aqui`

4. **Prueba la instalación**:
   ```bash
   python test_bot.py
   ```

5. **Ejecuta el bot**:
   ```bash
   python main.py
   ```

## 📁 Estructura del Proyecto

```
├── main.py                    # Aplicación principal del bot
├── config/                    # Configuración
│   ├── settings.py           # Configuraciones del bot
│   └── categories.py         # Categorías de comandos
├── cogs/                     # Módulos del bot
│   ├── moderation.py         # Comandos de moderación
│   ├── interactions.py       # Interacciones con GIFs
│   ├── user_commands.py      # Comandos de usuario
│   ├── fun_commands.py       # Comandos divertidos
│   ├── utility_commands.py   # Comandos de utilidad
│   └── community_commands.py # Comandos comunitarios
├── events/                   # Eventos del bot
│   ├── logging_events.py     # Eventos de logging
│   └── bot_events.py         # Eventos del bot
├── core/                     # Componentes core
│   └── bot.py               # Funcionalidad core
├── TODO.md                   # Lista de tareas
├── requirements.txt          # Dependencias de Python
├── railway.json             # Configuración de despliegue
└── README.md                # Este archivo
```

## 🎮 Comandos Disponibles

### 🛠️ Moderación
- `!ban <usuario> [razón]` - Banear a un usuario
- `!kick <usuario> [razón]` - Expulsar a un usuario
- `!mute <usuario> [tiempo] [razón]` - Silenciar a un usuario
- `!unmute <usuario>` - Des-silenciar a un usuario
- `!warn <usuario> [razón]` - Advertir a un usuario
- `!jail <usuario> [tiempo] [razón]` - Enviar a un usuario a la cárcel
- `!unjail <usuario>` - Sacar a un usuario de la cárcel

### 🎭 Interacciones (50+ comandos)
- `!hug <usuario>` - Abrazar a un usuario
- `!slap <usuario>` - Abofetear a un usuario
- `!kiss <usuario>` - Besar a un usuario
- `!pat <usuario>` - Acariciar a un usuario
- `!tickle <usuario>` - Hacer cosquillas
- `!feed <usuario>` - Alimentar a un usuario
- `!punch <usuario>` - Golpear a un usuario
- `!highfive <usuario>` - Chocar los cinco
- `!bite <usuario>` - Morder a un usuario
- `!shoot <usuario>` - Disparar a un usuario
- Y muchos más...

### 👤 Información de Usuario
- `!avatar [usuario]` - Ver avatar de un usuario
- `!userinfo [usuario]` - Información detallada de un usuario
- `!banner [usuario]` - Ver banner de un usuario
- `!serverinfo` - Información del servidor
- `!serverstats` - Estadísticas del servidor
- `!roleinfo <rol>` - Información de un rol
- `!channelinfo [canal]` - Información de un canal

### 🎲 Diversión y Entretenimiento
- `!roll <dados>` - Tirar dados (ej: 1d20, 2d6+3)
- `!coinflip` - Lanzar una moneda
- `!joke` - Obtener un chiste aleatorio
- `!fact` - Obtener un dato curioso
- `!meme` - Obtener un meme de programador
- `!8ball <pregunta>` - Preguntar a la bola 8 mágica
- `!choose <opción1, opción2, ...>` - Elegir entre opciones
- `!rate <algo>` - Calificar algo del 1-10
- `!password [longitud]` - Generar una contraseña segura

### 🔧 Utilidades
- `!ping` - Ver latencia del bot
- `!help [categoría]` - Mostrar ayuda organizada
- `!commands` - Lista simple de comandos
- `!invite` - Obtener enlace de invitación
- `!uptime` - Ver tiempo de actividad
- `!stats` - Ver estadísticas del bot
- `!suggest <sugerencia>` - Enviar una sugerencia
- `!bug <reporte>` - Reportar un bug
- `!info` - Información sobre el bot

### 🏘️ Comunidad
- `!poll <pregunta>` - Crear una encuesta
- `!remind <minutos> <mensaje>` - Establecer un recordatorio
- `!weather <ciudad>` - Ver el clima de una ciudad
- `!calc <expresión>` - Calculadora simple
- `!urban <término>` - Buscar en Urban Dictionary
- `!translate <idioma> <texto>` - Traducir texto
- `!covid [país]` - Estadísticas de COVID-19
- `!jokeapi [categoría]` - Chistes de JokeAPI

## ⚙️ Configuración

### Variables de Entorno (Opcional)
```bash
export DISCORD_TOKEN=tu_token_de_bot_aqui
export TENOR_API_KEY=tu_api_key_de_tenor  # Para GIFs
```

### Configuración en Código
- Edita `config/settings.py` para configuraciones avanzadas
- Modifica `config/categories.py` para personalizar categorías de ayuda

## 🚀 Despliegue

### Desarrollo Local
```bash
python main.py
```

### Despliegue en Producción
- Actualiza `railway.json` con tu token de bot
- Despliega en Railway, Heroku, o cualquier plataforma que soporte Python

## 📊 Estadísticas

- **Comandos:** 50+ comandos disponibles
- **Interacciones:** 50+ comandos de interacciones con GIFs
- **Idioma:** Comandos en español
- **Moderación:** Sistema completo de moderación
- **Diversión:** Entretenimiento variado para la comunidad

## 🐛 Solución de Problemas

### Problemas Comunes
1. **El bot no responde a comandos**
   - Verifica que el token del bot sea correcto
   - Asegúrate de que el bot tenga permisos en el servidor
   - Revisa que los comandos estén registrados correctamente

2. **Error de dependencias**
   - Ejecuta `pip install -r requirements.txt`
   - Verifica la versión de Python (3.8+)

3. **Error de token**
   - Reemplaza `"YOUR_BOT_TOKEN_HERE"` en `main.py` con tu token real
   - O usa variables de entorno

## 🤝 Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu feature
3. Haz tus cambios
4. Prueba exhaustivamente
5. Envía un pull request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Para soporte y preguntas:
- Revisa la sección de solución de problemas
- Revisa los logs para mensajes de error
- Prueba con el script de test incluido
- Revisa la documentación de discord.py para problemas de API

---

**¡Feliz boteo!** 🐨✨
