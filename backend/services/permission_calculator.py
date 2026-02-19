from backend.models.guild import Guild
from backend.models.channel import Channel
from backend.models.role import Role
from backend.models.permission_overwrite import PermissionOverwrite

class PermissionCalculator:
    """
    Kapselt die Logik zur Berechnung effektiver Berechtigungen.
    Orientiert sich an der offiziellen Discord-Logik.
    """

    @staticmethod
    def calculate_base_permissions(member_roles: list[Role], guild_id: str) -> int:
        """
        Berechnet die Basis-Berechtigungen eines Members im Kontext einer Guild (ohne Channel-Regeln).
        1. @everyone permissions
        2. + alle Rollen des Members (ODER-verknüpft)
        3. Administrator-Check (Bit 3)
        """
        if not member_roles:
            return 0

        # Annahme: @everyone Rolle ist in member_roles enthalten (id == guild_id)
        # In unserer DB ist is_everyone oder id=guild_id nicht explizit markiert, 
        # aber Discord Logik sagt: base = everyone_role.permissions
        
        # Wir summieren einfach alle Bits.
        permissions = 0
        for role in member_roles:
            permissions |= int(role.permissions)

        # Wenn Administrator (Bit 3 aka 0x8), dann alles erlauben?
        # Discord API sagt: Administrator überschreibt alles (auch Channel Denys).
        # Wir geben hier das Bitfield zurück. Der Check auf Admin passiert meist am Ende oder der Caller prüft es.
        
        return permissions

    @staticmethod
    def calculate_channel_permissions(
        base_permissions: int,
        channel: Channel,
        member_id: str,
        member_roles: list[Role]
    ) -> int:
        """
        Berechnet die effektiven Rechte in einem Kanal.
        
        Logic Flow:
        1. Base Permissions
        2. If Administrator -> Return ALL
        3. Apply @everyone Overwrite (deny then allow)
        4. Apply Role Overwrites (allow/deny aggregated, then applied: deny then allow)
        5. Apply Member Overwrite (deny then allow)
        """
        
        ADMINISTRATOR = 0x8
        if base_permissions & ADMINISTRATOR:
            return -1 # Oder eine Konstante für "ALL" (in Python int sind unendlich, Discord max ist ~53 bits)
            # Wir geben einfach alle Bits zurück, die wir kennen, oder behalten das Admin Bit.
            # Um konsistent zu bleiben: return base_permissions (da Admin enthalten ist)
            return base_permissions

        permissions = base_permissions
        overwrites = channel.overwrites or []

        # 3. @everyone Overwrite
        # In unserem Modell ist target_id == guild_id für @everyone Overwrite
        everyone_overwrite = next((ow for ow in overwrites if ow.target_id == channel.guild_id), None)
        if everyone_overwrite:
            permissions &= ~int(everyone_overwrite.deny)
            permissions |= int(everyone_overwrite.allow)

        # 4. Role Overwrites
        # Wir müssen Allow und Deny aller Rollen des Members zusammenrechnen.
        role_allow = 0
        role_deny = 0
        
        member_role_ids = {r.id for r in member_roles}
        
        for ow in overwrites:
            if ow.target_type == 'role' and ow.target_id in member_role_ids and ow.target_id != channel.guild_id:
                role_allow |= int(ow.allow)
                role_deny |= int(ow.deny)

        permissions &= ~role_deny
        permissions |= role_allow

        # 5. Member Overwrite
        member_overwrite = next((ow for ow in overwrites if ow.target_type == 'member' and ow.target_id == member_id), None)
        if member_overwrite:
            permissions &= ~int(member_overwrite.deny)
            permissions |= int(member_overwrite.allow)

        return permissions

    @staticmethod
    def detect_conflicts(channel: Channel, role: Role) -> list[dict]:
        """
        Erkennt Konflikte zwischen Rollen-Rechten und Kanal-Overwrites.
        Konflikt definiert als: Rolle erlaubt X, aber Kanal verweigert X explizit.
        """
        conflicts = []
        
        # Finde Overwrite für diese Rolle in diesem Channel
        overwrite = next((ow for ow in channel.overwrites if ow.target_type == 'role' and ow.target_id == role.id), None)
        
        if not overwrite:
            return []
            
        role_perms = int(role.permissions)
        deny_perms = int(overwrite.deny)
        
        # Check all bits (simplified loop or specific check)
        # Wir prüfen nur wichtige Permissions oder alle?
        # Alle Bits iteration:
        for i in range(53): # Discord permissions go up to bit ~50
            bit_mask = 1 << i
            
            has_role_perm = (role_perms & bit_mask) == bit_mask
            has_deny_perm = (deny_perms & bit_mask) == bit_mask
            
            if has_role_perm and has_deny_perm:
                 conflicts.append({
                     "permission_bit": i,
                     "role_id": role.id,
                     "channel_id": channel.id,
                     "reason": "Role allows but Channel denies"
                 })
                 
        return conflicts

    @staticmethod
    def explain_permission(permission_bit: int) -> str:
        """Liefert einen lesbaren Namen für ein Permission-Bit (Stub)."""
        # Hier könnte man eine Map nutzen.
        # Beispiel: 3 -> ADMINISTRATOR
        # Für den Prototyp geben wir "BIT_X" zurück oder hardcoden ein paar.
        known = {
            3: "ADMINISTRATOR",
            10: "VIEW_CHANNEL",
            11: "SEND_MESSAGES"
        }
        return known.get(permission_bit, f"BIT_{permission_bit}")
