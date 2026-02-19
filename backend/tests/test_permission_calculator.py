import pytest
from backend.services.permission_calculator import PermissionCalculator
from backend.models.role import Role
from backend.models.channel import Channel
from backend.models.permission_overwrite import PermissionOverwrite

# Mock Objects
class MockRole(Role):
    def __init__(self, id, permissions):
        self.id = id
        self.permissions = str(permissions)

class MockChannel(Channel):
    def __init__(self, id, guild_id, overwrites=None):
        self.id = id
        self.guild_id = guild_id
        self.overwrites = overwrites or []

class MockOverwrite(PermissionOverwrite):
    def __init__(self, target_id, target_type, allow, deny):
        self.target_id = target_id
        self.target_type = target_type
        self.allow = str(allow)
        self.deny = str(deny)

@pytest.mark.asyncio
async def test_base_permissions():
    """Test calculation of base permissions from roles."""
    # Role A: 1 (Create Instant Invite)
    # Role B: 4 (Ban Members)
    roles = [MockRole("r1", 1), MockRole("r2", 4)]
    
    perms = PermissionCalculator.calculate_base_permissions(roles, "guild1")
    assert perms == 5 # 1 | 4 = 5

@pytest.mark.asyncio
async def test_admin_override():
    """Test that Administrator permission (0x8) overrides channel overwrites."""
    # Role with Administrator (8)
    roles = [MockRole("admin", 8)]
    base = PermissionCalculator.calculate_base_permissions(roles, "guild1")
    
    # Channel with deny all for everyone
    # But wait, logic for admin override happens in calculate_channel_permissions
    
    channel = MockChannel("c1", "guild1")
    # Overwrite: Deny everything (let's say bit 1) for this role
    ow = MockOverwrite("admin", "role", 0, 1)
    channel.overwrites = [ow]
    
    effective = PermissionCalculator.calculate_channel_permissions(base, channel, "u1", roles)
    assert effective == -1 # Admin grants ALL permissions (represented as -1 here)

@pytest.mark.asyncio
async def test_channel_overwrites():
    """Test complex channel overwrite logic."""
    # Base: 0
    # @everyone overwrite: allow 1 (Create Invite)
    # Role overwrite: deny 1, allow 2 (Kick Members - hypothetical bit)
    # Member overwrite: allow 4 (Ban Members)
    
    guild_id = "g1"
    member_id = "u1"
    role_id = "r1"
    
    roles = [MockRole(role_id, 0)]
    base = 0
    
    # Overwrites
    ow_everyone = MockOverwrite(guild_id, "role", 1, 0) # everyone allow 1
    ow_role = MockOverwrite(role_id, "role", 2, 1)     # role deny 1, allow 2
    ow_member = MockOverwrite(member_id, "member", 4, 0) # member allow 4
    
    channel = MockChannel("c1", guild_id, [ow_everyone, ow_role, ow_member])
    
    # 1. Base = 0
    # 2. Everyone: +1 -> 1
    # 3. Role: Deny 1 -> 0, Allow 2 -> 2
    # 4. Member: Allow 4 -> 6
    # Estimated Result: 6 (Bits 2 and 4 set)
    
    effective = PermissionCalculator.calculate_channel_permissions(base, channel, member_id, roles)
    assert effective == 6
