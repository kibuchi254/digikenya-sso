from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base # Assuming 'Base' is your declarative base

# --- ASSOCIATION OBJECT CLASS (Resolves ArgumentError) ---
# This class acts as the join table, allowing you to add extra attributes
# (though none are currently defined). It MUST have a Primary Key.
class UserRole(Base):
    """Association object for the many-to-many relationship between User and Role."""
    __tablename__ = "user_roles_assoc"

    # Composite Primary Key: Combination of user_id and role_id must be unique
    user_id = Column(
        Integer, 
        ForeignKey("users.id"), 
        primary_key=True # FIX: Must be part of the primary key
    )
    role_id = Column(
        Integer, 
        ForeignKey("roles.id"), 
        primary_key=True # FIX: Must be part of the primary key
    )

    # Relationships to the parent objects
    user = relationship("User", back_populates="roles") # Links back to the User object
    role = relationship("Role", back_populates="users") # Links back to the Role object

# --- ROLE MODEL ---
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = Column(String)  # JSON string of permissions
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    # Relationships
    tenant = relationship("Tenant", back_populates="roles")
    
    # Relationship to the association object (UserRole)
    users = relationship("UserRole", back_populates="role")