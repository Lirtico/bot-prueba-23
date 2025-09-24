# 🚂 Despliegue en Railway

Este bot está configurado para desplegarse automáticamente en **Railway** con soporte completo para comandos slash.

## ✅ Configuración Requerida

### 1. Variables de Entorno en Railway

1. Ve a tu proyecto en **Railway**
2. **Settings > Environment Variables**
3. Agrega esta variable:
   ```
   DISCORD_BOT_TOKEN = tu_token_real_aqui
   ```

### 2. Despliegue Automático

1. **Sube tu código** a GitHub/GitLab
2. **Conecta Railway** a tu repositorio
3. **Railway detectará** `railway.json` automáticamente
4. **¡El bot se desplegará!**

## 🔧 Configuración Actual

### railway.json
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### main.py
- ✅ **Token desde variables de entorno**
- ✅ **Sincronización automática** de comandos slash
- ✅ **Logging detallado** para debugging
- ✅ **Manejo de errores** robusto

## 📋 Comandos Slash Incluidos

Cuando el bot se despliegue correctamente, aparecerán estos comandos:

- `/help` - Sistema de ayuda interactivo
- `/ping` - Verificar latencia
- `/info` - Información del bot
- `/stats` - Estadísticas del bot
- `/invite` - Enlace de invitación
- `/uptime` - Tiempo de actividad
- `/suggest` - Enviar sugerencias
- `/bug` - Reportar bugs

## 🚨 Solución de Problemas

### Si los comandos slash no aparecen:
1. **Espera 1-2 minutos** para que Discord sincronice
2. **Verifica los logs** en Railway dashboard
3. **Asegúrate de que el bot tenga permisos** `applications.commands`
4. **Revisa que el token** esté configurado correctamente

### Verificación de Logs:
En los logs de Railway deberías ver:
```
✅ Loaded cog: cogs.slash_commands
📋 Slash commands in tree before sync: 8
✅ Synced 8 slash commands globally
📋 Slash commands in tree after sync: 8
```

## 🎯 ¿Qué hace esta configuración?

- **✅ Carga automática** de todos los cogs
- **✅ Sincronización global** de comandos slash
- **✅ Reinicio automático** si hay errores
- **✅ Variables de entorno** seguras
- **✅ Logging completo** para debugging

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway dashboard
2. Verifica que el token esté correcto
3. Asegúrate de que el bot tenga los permisos necesarios
4. Espera unos minutos para que Discord sincronice los comandos

¡Tu bot Koala está listo para Railway! 🐨✨
