from io import StringIO

class SqlBuilder:
    def __init__(self, table, alias = None):
        self.table = table
        self.alias = alias
        self.selects = []
        self.joins = []
        self.whereClauses = []
        self.groupColumns = []
        self.orderColumns = []
        self.order = ""
        self.params = {}
    
    def Select(self, column, alias = None):
        if (alias is not None):
            self.selects.append(f"{column} {alias}")
        else:
            self.selects.append(column)

        return self
    
    def Join(self, table, joinClause, alias = None):
        self.joins.append({'table': table, 'joinClause': joinClause, 'alias': alias})

        return self

    def Where(self, clause):
        self.whereClauses.append(clause)

        return self

    def Param(self, name, value):
        self.params[name] = value

        return self

    def Build(self):
        sqlStream = StringIO()

        sqlStream.write("SELECT ")

        if len(self.selects) > 0:
            sqlStream.write(", ".join(self.selects))
        else:
            sqlStream.write("*")
        
        sqlStream.write(f" FROM {self.table} ")

        if self.alias is not None:
            sqlStream.write(f"{self.alias} ")
        
        if len(self.joins) > 0:
            sqlStream.write("JOIN ")
            for join in self.joins:
                sqlStream.write(f"{join['table']} ")

                if join['alias'] is not None:
                    sqlStream.write(f"{join['alias']} ")

                sqlStream.write(f"ON {join['joinClause']} ")

        if len(self.whereClauses) > 0:
            sqlStream.write("WHERE ")
            sqlStream.write(" AND ".join(self.whereClauses))

        return sqlStream.getvalue()

sql = SqlBuilder("Compra", "c")
sql.Select("c.Total", "TotalCompra")
sql.Join("c.CompraItem", "c.Id = ci.Compra", "ci")
sql.Where("c.DataCriacao > :dataCriacao")
sql.Where("c.Cliente = :cliente")

print(sql.Build())
