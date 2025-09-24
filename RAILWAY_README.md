# 🚂 Despliegue en Railway

Este bot está configurado para desplegarse en **Railway** automáticamente.

## 📋 Configuración Requerida

### 1. **Variables de Entorno**
En tu proyecto de Railway, ve a **Settings > Environment Variables** y agrega:

```
DISCORD_BOT_TOKEN = tu_token_de_discord_aqui
```

### 2. **Configuración del Proyecto**
El archivo `railway.json` ya está configurado con:
- ✅ Comando de inicio: `python main.py`
- ✅ Variables de entorno configuradas
- ✅ Sincronización automática de comandos slash

## 🚀 Despliegue Automático

1. **Sube tu código** a GitHub/GitLab
2. **Conecta Railway** a tu repositorio
3. **Railway detectará automáticamente** la configuración
4. **El bot se desplegará** y sincronizará los comandos slash

## 🔧 Comandos Slash

Los comandos slash se sincronizan automáticamente cuando el bot inicia:

- `/help` - Sistema de ayuda interactivo
- `/ping` - Verificar latencia
- `/info` - Información del bot
- `/stats` - Estadísticas del servidor
- `/invite` - Enlace de invitación
- `/uptime` - Tiempo de actividad
- `/suggest` - Sistema de sugerencias
- `/bug` - Reporte de bugs

## 📊 Monitoreo

- **Logs en tiempo real** disponibles en Railway dashboard
- **Reinicio automático** en caso de errores
- **Sincronización automática** de comandos slash

## 🐛 Solución de Problemas

### Si `/help` no aparece:
1. Verifica que el token esté configurado correctamente
2. Espera 1-2 minutos para que Discord sincronice
3. Revisa los logs en Railway dashboard

### Si el bot no inicia:
1. Verifica que `DISCORD_BOT_TOKEN` esté configurado
2. Revisa los logs para errores de importación
3. Asegúrate de que todos los archivos estén subidos

## ✨ Características de Railway

- ✅ **Despliegue automático** desde Git
- ✅ **Variables de entorno** seguras
- ✅ **Logs en tiempo real**
- ✅ **Reinicio automático** en errores
- ✅ **Escalabilidad** automática
- ✅ **Base de datos** integrada (si necesitas)

¡Tu bot Koala está listo para Railway! 🐨✨
