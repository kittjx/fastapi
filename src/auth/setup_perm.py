
# Helper to create initial permissions

from sqlmodel import select
from db.session import DBSession
from user.model import Permission, Role, RolePermissionLink


async def create_initial_permissions(session: DBSession):
    """Create initial permissions and roles"""
    permissions = [
        Permission(name="book.read", description="View books"),
        Permission(name="book.write", description="Create/update books"),
        Permission(name="book.delete", description="Delete books"),
    ]
    
    for perm in permissions:
        session.add(perm)
    
    # Create roles
    admin_role = Role(name="admin", description="Administrator")
    user_role = Role(name="user", description="Regular user")
    moderator_role = Role(name="moderator", description="Moderator")
    
    session.add_all([admin_role, user_role, moderator_role])
    await session.commit()
    
    # Assign permissions to roles
    # Admin gets all permissions
    result = await session.exec(select(Permission))
    admin_permissions = result.all()
    for perm in admin_permissions:
        link = RolePermissionLink(role_id=admin_role.id, permission_id=perm.id)
        session.add(link)
    
    # User gets basic read permissions
    result = await session.exec(
        select(Permission).where(Permission.name.in_(["book.read"]))
    )
    user_permissions = result.all()
    for perm in user_permissions:
        link = RolePermissionLink(role_id=user_role.id, permission_id=perm.id)
        session.add(link)
    
    # Moderator gets read/write permissions
    result = await session.exec(
        select(Permission).where(Permission.name.in_([
            "book.read", "book.write"
        ]))
    )
    mod_permissions = result.all()
    for perm in mod_permissions:
        link = RolePermissionLink(role_id=moderator_role.id, permission_id=perm.id)
        session.add(link)
    
    await session.commit()


if __name__ == "__main__":
    import asyncio
    from db.session import get_async_session

    async def main():
        session_generator = get_async_session()
        session = await session_generator.__anext__()
        try:
            await create_initial_permissions(session)
        finally:
            await session_generator.aclose()
        print("Initial permissions and roles created successfully.")

    asyncio.run(main())
