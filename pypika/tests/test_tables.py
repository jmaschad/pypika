import unittest

from pypika import (
    Database,
    Schema,
    Table,
    Tables,
)

__author__ = "Timothy Heys"
__email__ = "theys@kayak.com"


class TableStructureTests(unittest.TestCase):
    def test_table_sql(self):
        table = Table("test_table")

        self.assertEqual('"test_table"', str(table))

    def test_table_with_alias(self):
        table = Table("test_table").as_("my_table")

        self.assertEqual(
            '"test_table" "my_table"', table.get_sql(with_alias=True, quote_char='"')
        )

    def test_schema_table_attr(self):
        table = Schema("x_schema").test_table

        self.assertEqual('"x_schema"."test_table"', str(table))

    def test_table_with_schema_arg(self):
        table = Table("test_table", schema=Schema("x_schema"))

        self.assertEqual('"x_schema"."test_table"', str(table))

    def test_database_schema_table_attr(self):
        table = Database("x_db").x_schema.test_table

        self.assertEqual('"x_db"."x_schema"."test_table"', str(table))

    def test_table_with_schema_and_schema_parent_arg(self):
        table = Table("test_table", schema=Schema("x_schema", parent=Database("x_db")))

        self.assertEqual('"x_db"."x_schema"."test_table"', str(table))


class TableEqualityTests(unittest.TestCase):
    def test_tables_equal_by_name(self):
        t1 = Table("t")
        t2 = Table("t")

        self.assertEqual(t1, t2)

    def test_tables_equal_by_schema_and_name(self):
        t1 = Table("t", schema="a")
        t2 = Table("t", schema="a")

        self.assertEqual(t1, t2)

    def test_tables_equal_by_schema_and_name_using_schema(self):
        a = Schema("a")
        t1 = Table("t", schema=a)
        t2 = Table("t", schema=a)

        self.assertEqual(t1, t2)

    def test_tables_equal_by_schema_and_name_using_schema_with_parent(self):
        parent = Schema("parent")
        a = Schema("a", parent=parent)
        t1 = Table("t", schema=a)
        t2 = Table("t", schema=a)

        self.assertEqual(t1, t2)

    def test_tables_not_equal_by_schema_and_name_using_schema_with_different_parents(
        self,
    ):
        parent = Schema("parent")
        a = Schema("a", parent=parent)
        t1 = Table("t", schema=a)
        t2 = Table("t", schema=Schema("a"))

        self.assertNotEqual(t1, t2)

    def test_tables_not_equal_with_different_schemas(self):
        t1 = Table("t", schema="a")
        t2 = Table("t", schema="b")

        self.assertNotEqual(t1, t2)

    def test_tables_not_equal_with_different_names(self):
        t1 = Table("t", schema="a")
        t2 = Table("q", schema="a")

        self.assertNotEqual(t1, t2)

    def test_many_tables_with_alias(self):
        tables_data = [("table1", "t1"), ("table2", "t2"), ("table3", "t3")]
        tables = Tables(*tables_data)
        for el in tables:
            self.assertIsNotNone(el.alias)

    def test_many_tables_without_alias(self):
        tables_data = ["table1", "table2", "table3"]
        tables = Tables(*tables_data)
        for el in tables:
            self.assertIsNone(el.alias)

    def test_many_tables_with_or_not_alias(self):
        tables_data = [("table1", "t1"), ("table2"), "table3"]
        tables = Tables(*tables_data)
        for i in range(len(tables)):
            if isinstance(tables_data[i], tuple):
                self.assertIsNotNone(tables[i].alias)
            else:
                self.assertIsNone(tables[i].alias)
