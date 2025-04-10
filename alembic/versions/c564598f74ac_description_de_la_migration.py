"""Description de la migration

Revision ID: c564598f74ac
Revises: 
Create Date: 2025-03-28 01:16:36.650733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c564598f74ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('thematiques',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_thematiques_id'), 'thematiques', ['id'], unique=False)
    op.create_index(op.f('ix_thematiques_nom'), 'thematiques', ['nom'], unique=False)
    op.create_table('types_exercice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_types_exercice_id'), 'types_exercice', ['id'], unique=False)
    op.create_index(op.f('ix_types_exercice_nom'), 'types_exercice', ['nom'], unique=False)
    op.create_table('utilisateurs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('nom', sa.String(), nullable=True),
    sa.Column('prenom', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_utilisateurs_email'), 'utilisateurs', ['email'], unique=True)
    op.create_index(op.f('ix_utilisateurs_id'), 'utilisateurs', ['id'], unique=False)
    op.create_table('exercices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titre', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('difficulte', sa.Integer(), nullable=True),
    sa.Column('duree_estimee', sa.Integer(), nullable=True),
    sa.Column('thematique_id', sa.Integer(), nullable=True),
    sa.Column('type_exercice_id', sa.Integer(), nullable=True),
    sa.Column('createur_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['createur_id'], ['utilisateurs.id'], ),
    sa.ForeignKeyConstraint(['thematique_id'], ['thematiques.id'], ),
    sa.ForeignKeyConstraint(['type_exercice_id'], ['types_exercice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercices_id'), 'exercices', ['id'], unique=False)
    op.create_index(op.f('ix_exercices_titre'), 'exercices', ['titre'], unique=False)
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enonce', sa.String(), nullable=True),
    sa.Column('points_max', sa.Integer(), nullable=True),
    sa.Column('exercice_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exercice_id'], ['exercices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_table('tentatives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('utilisateur_id', sa.Integer(), nullable=True),
    sa.Column('exercice_id', sa.Integer(), nullable=True),
    sa.Column('date_debut', sa.DateTime(), nullable=True),
    sa.Column('date_fin', sa.DateTime(), nullable=True),
    sa.Column('note_finale', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['exercice_id'], ['exercices.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateurs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tentatives_id'), 'tentatives', ['id'], unique=False)
    op.create_table('corrections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('solution', sa.String(), nullable=True),
    sa.Column('explication', sa.String(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question_id')
    )
    op.create_index(op.f('ix_corrections_id'), 'corrections', ['id'], unique=False)
    op.create_table('reponses_utilisateur',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contenu', sa.String(), nullable=True),
    sa.Column('est_correcte', sa.Boolean(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('tentative_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['tentative_id'], ['tentatives.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reponses_utilisateur_id'), 'reponses_utilisateur', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reponses_utilisateur_id'), table_name='reponses_utilisateur')
    op.drop_table('reponses_utilisateur')
    op.drop_index(op.f('ix_corrections_id'), table_name='corrections')
    op.drop_table('corrections')
    op.drop_index(op.f('ix_tentatives_id'), table_name='tentatives')
    op.drop_table('tentatives')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_exercices_titre'), table_name='exercices')
    op.drop_index(op.f('ix_exercices_id'), table_name='exercices')
    op.drop_table('exercices')
    op.drop_index(op.f('ix_utilisateurs_id'), table_name='utilisateurs')
    op.drop_index(op.f('ix_utilisateurs_email'), table_name='utilisateurs')
    op.drop_table('utilisateurs')
    op.drop_index(op.f('ix_types_exercice_nom'), table_name='types_exercice')
    op.drop_index(op.f('ix_types_exercice_id'), table_name='types_exercice')
    op.drop_table('types_exercice')
    op.drop_index(op.f('ix_thematiques_nom'), table_name='thematiques')
    op.drop_index(op.f('ix_thematiques_id'), table_name='thematiques')
    op.drop_table('thematiques')
    # ### end Alembic commands ###
