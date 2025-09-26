# TODO List for Discord Bot Interactions Fix

## Completed Tasks
- [x] Update all interaction commands requiring a member to make the member parameter optional
- [x] Add error check for when member is None: send "❌ Debes mencionar a alguien para usar este comando."
- [x] Ensure self-checks are preserved and error checks are added after them
- [x] Add new !hi command with optional member, anime wave GIF, custom descriptions, self-check, try-except fallback
- [x] Verify syntax with py_compile
- [x] Update !sleep, !smug, !smile, !angry to make member optional and change embed message to solitary when no member is mentioned
- [x] Verify syntax with py_compile after updates

## Next Steps
- [ ] Test the bot to ensure commands work correctly (e.g., run the bot and test !slap without member, with member, self)
- [ ] Test !hi command specifically
- [ ] Test updated solitary commands (!sleep, !smug, !smile, !angry)
- [ ] If issues, debug and fix
