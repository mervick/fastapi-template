from enum import StrEnum


class OnDelete(StrEnum):
    """
    Cascade:
    When a referenced row in the parent table is deleted, all corresponding rows in the
     child table will also be deleted.

    SetNull:
    When a referenced row in the parent table is deleted, the foreign key columns in the corresponding rows of the child
     table will be set to NULL.

    SetDefault:
    Similar to SET NULL, but sets the foreign key columns to their default values.

    Restrict:
    Prevents deletion of a referenced row in the parent table if there are corresponding rows in the child table.

    NoAction:
    Similar to RESTRICT, it prevents deletion of a referenced row in the parent table if there are corresponding rows in
     the child table.

    Dump:
    A non-standard option that can be used to simulate a database feature that is not natively supported
    """

    CASCADE = "CASCADE"
    SET_NULL = "SET NULL"
    SET_DEFAULT = "SET DEFAULT"
    RESTRICT = "RESTRICT"
    NO_ACTION = "NO ACTION"
    DUMP = "DUMP"
