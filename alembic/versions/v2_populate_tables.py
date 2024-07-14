from typing import Sequence, Union

from script_populate_database import PopulateScript

# revision identifiers, used by Alembic.
revision: str = "2e1ae80b92bb"
down_revision: Union[str, None] = "4ea92ec510a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    PopulateScript()


def downgrade() -> None:
    pass
