# Command categories for help system
COMMAND_CATEGORIES = {
    "slash": {
        "name": "⚡ Commands Slash",
        "description": "Comandos slash (/) modernos e interactivos",
        "commands": {
            "`/help`": "Sistema de ayuda interactivo con botones",
            "`/ping`": "Verificar latencia del bot",
            "`/info`": "Información del bot",
            "`/stats`": "Estadísticas del bot",
            "`/invite`": "Obtener enlace de invitación",
            "`/uptime`": "Tiempo de actividad del bot",
            "`/suggest`": "Enviar sugerencias",
            "`/bug`": "Reportar bugs",
            "`/slap <usuario>`": "Abofetear a un usuario con GIF",
            "`/hug <usuario>`": "Abrazar a un usuario con GIF",
            "`/kiss <usuario>`": "Besar a un usuario con GIF",
            "`/pat <usuario>`": "Acariciar a un usuario con GIF",
            "`/cuddle <usuario>`": "Acurrucar a un usuario con GIF"
        },
        "color": 0x5865f2
    },
    "roleplay": {
        "name": "🎭 Roleplay",
        "description": "Comandos de interacciones con GIFs anime",
        "commands": {
            "`!slap <usuario>`": "Abofetear a un usuario",
            "`!hug <usuario>`": "Abrazar a un usuario",
            "`!kiss <usuario>`": "Besar a un usuario",
            "`!pat <usuario>`": "Acariciar a un usuario",
            "`!tickle <usuario>`": "Hacer cosquillas a un usuario",
            "`!feed <usuario>`": "Alimentar a un usuario",
            "`!punch <usuario>`": "Golpear a un usuario",
            "`!highfive <usuario>`": "Chocar los cinco con un usuario",
            "`!bite <usuario>`": "Morder a un usuario",
            "`!shoot <usuario>`": "Disparar a un usuario",
            "`!wave <usuario>`": "Saludar a un usuario",
            "`!happy <usuario>`": "Estar feliz con un usuario",
            "`!peck <usuario>`": "Picotear a un usuario",
            "`!lurk <usuario>`": "Acechar a un usuario",
            "`!sleep <usuario>`": "Dormir con un usuario",
            "`!wink <usuario>`": "Guiñar a un usuario",
            "`!yawn <usuario>`": "Bostezar con un usuario",
            "`!nom <usuario>`": "Nom a un usuario",
            "`!yeet <usuario>`": "Yeet a un usuario",
            "`!think <usuario>`": "Pensar en un usuario",
            "`!bored <usuario>`": "Aburrirse con un usuario",
            "`!blush <usuario>`": "Sonrojarse con un usuario",
            "`!stare <usuario>`": "Mirar a un usuario",
            "`!nod <usuario>`": "Asentir a un usuario",
            "`!handhold <usuario>`": "Tomar la mano de un usuario",
            "`!smug <usuario>`": "Ser presumido con un usuario",
            "`!spank <usuario>`": "Azotar a un usuario",
            "`!nutkick <usuario>`": "Dar una patada en las bolas a un usuario",
            "`!shrug <usuario>`": "Encogerse de hombros con un usuario",
            "`!poke <usuario>`": "Picar a un usuario",
            "`!smile <usuario>`": "Sonreír a un usuario",
            "`!facepalm <usuario>`": "Hacer facepalm con un usuario",
            "`!cuddle <usuario>`": "Acurrucar a un usuario",
            "`!baka <usuario>`": "Llamar baka a un usuario",
            "`!angry <usuario>`": "Enojarse con un usuario",
            "`!run <usuario>`": "Correr con un usuario",
            "`!nope <usuario>`": "Decir nope a un usuario",
            "`!handshake <usuario>`": "Estrechar la mano con un usuario",
            "`!cry <usuario>`": "Llorar con un usuario",
            "`!pout <usuario>`": "Hacer pucheros con un usuario",
            "`!thumbsup <usuario>`": "Dar thumbs up a un usuario",
            "`!laugh <usuario>`": "Reírse de un usuario"
        },
        "color": 0xff1493
    },
    "moderation": {
        "name": "🛠️ Moderación",
        "description": "Comandos para moderar el servidor",
        "commands": {
            "`!purge <cantidad>`": "Eliminar mensajes",
            "`!kick <usuario> [razón]`": "Expulsar a un usuario",
            "`!ban <usuario> [razón]`": "Banear a un usuario",
            "`!unban <user_id>`": "Desbanear a un usuario",
            "`!warn <usuario> [razón]`": "Advertir a un usuario",
            "`!jail <usuario> [razón]`": "Enviar a un usuario a la cárcel",
            "`!unjail <usuario> [razón]`": "Liberar a un usuario de la cárcel",
            "`!jailstatus`": "Ver usuarios en la cárcel"
        },
        "color": 0xff0000
    },
    "user": {
        "name": "👤 Usuario",
        "description": "Comandos relacionados con usuarios",
        "commands": {
            "`!avatar [@usuario]`": "Obtener el avatar de un usuario",
            "`!userinfo [@usuario]`": "Obtener información de un usuario",
            "`!banner [@usuario]`": "Obtener el banner de un usuario"
        },
        "color": 0x0099ff
    },
    "fun": {
        "name": "🎲 Diversión",
        "description": "Comandos de entretenimiento",
        "commands": {
            "`!roll <dados>`": "Tirar dados (ej: 1d20)",
            "`!coinflip`": "Lanzar una moneda",
            "`!joke`": "Obtener un chiste aleatorio",
            "`!fact`": "Obtener un dato curioso",
            "`!meme`": "Obtener un meme de programador",
            "`!8ball <pregunta>`": "Preguntar a la bola 8 mágica",
            "`!choose <opción1, opción2>`": "Elegir entre opciones",
            "`!rate <algo>`": "Calificar algo del 1-10",
            "`!reverse <texto>`": "Invertir texto",
            "`!password [longitud]`": "Generar contraseña segura",
            "`!color [hex]`": "Información de color",
            "`!emojify <texto>`": "Convertir texto a emojis"
        },
        "color": 0xff9900
    },
    "utility": {
        "name": "🔧 Utilidad",
        "description": "Comandos útiles y herramientas",
        "commands": {
            "`!say <mensaje>`": "Hacer que el bot diga algo",
            "`!ping`": "Verificar la latencia del bot",
            "`!help`": "Mostrar esta ayuda",
            "`!commands`": "Lista simple de comandos"
        },
        "color": 0x00ff00
    },
    "community": {
        "name": "🏘️ Comunidad",
        "description": "Comandos para la comunidad",
        "commands": {
            "`!poll <pregunta>`": "Crear una encuesta",
            "`!remind <minutos> <mensaje>`": "Establecer un recordatorio",
            "`!weather <ciudad>`": "Obtener información del clima",
            "`!calc <expresión>`": "Calculadora simple",
            "`!urban <término>`": "Buscar en Urban Dictionary",
            "`!translate <idioma> <texto>`": "Traducir texto",
            "`!covid [país]`": "Estadísticas de COVID-19",
            "`!jokeapi [categoría]`": "Chistes de JokeAPI"
        },
        "color": 0xff69b4
    },
    "info": {
        "name": "📊 Información",
        "description": "Comandos de información",
        "commands": {
            "`!serverinfo`": "Obtener información del servidor",
            "`!serverstats`": "Estadísticas detalladas del servidor",
            "`!roleinfo <rol>`": "Obtener información de un rol",
            "`!channelinfo [canal]`": "Obtener información de un canal"
        },
        "color": 0x9932cc
    }
}
