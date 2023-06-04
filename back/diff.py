import re

"""
Example
"""
# Upgrade -> get_diff(commit1, commit2)
# Downgrade -> get_diff(commit2, commit1)


# Read SQL file
def readSqlFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        print(command)
        
    return sqlFile



def parse_sql_script(sql_script):
    table_dict = {}
    current_table = ""
    current_attributes = {}

    create_table_pattern = re.compile(r"CREATE TABLE `(\w+)` \((.*?)\)(?:\s*ENGINE.*?)?;", re.DOTALL)
    attribute_pattern = re.compile(r"\n  `(\S*?)` (.*?)(,|\n)(?![^()]*\))", re.DOTALL)
    primary_key_pattern = re.compile(r"PRIMARY KEY \((.*?)\)", re.DOTALL)
    foreign_key_pattern = re.compile(
        r"CONSTRAINT `(\S*?)` FOREIGN KEY \((\S*?)\) REFERENCES `(\S*?)` \(`(\S*?)`\)"
        r"(?:\s*ON DELETE (SET NULL|SET DEFAULT|CASCADE|NO ACTION))?"
        r"(?:\s*ON UPDATE (SET NULL|SET DEFAULT|CASCADE|NO ACTION))?",
        re.DOTALL
    )
    check_pattern = re.compile(r"CONSTRAINT `(\S*?)` CHECK (.*?)\)\n", re.DOTALL)
    unique_key_pattern = re.compile(r"UNIQUE KEY `(\S*?)` \((.*?)\)", re.DOTALL)

    matches = re.findall(create_table_pattern, sql_script)
    for match in matches:
        current_table = match[0]
        current_attributes = {}

        attribute_matches = re.findall(attribute_pattern, match[1])
        for attribute_match in attribute_matches:
            attribute_name = attribute_match[0]
            attribute_definition = attribute_match[1].strip()
            # Check if attribute_match contains 'REFERENCES' or 'CHECK'
            if 'REFERENCES' in attribute_name or 'CHECK' in attribute_name:
                continue  # Skip and ignore the match
            current_attributes[attribute_name] = attribute_definition

        primary_key_match = re.search(primary_key_pattern, match[1])
        if primary_key_match:
            primary_key_columns = primary_key_match.group(1).split(',')
            current_attributes['PRIMARY KEY'] = [col.strip('`') for col in primary_key_columns]

        foreign_key_matches = re.findall(foreign_key_pattern, match[1])
        foreign_key_dict = {}
        for foreign_key_match in foreign_key_matches:
            constraint_name = foreign_key_match[0]
            foreign_key_columns = foreign_key_match[1]
            referenced_table = foreign_key_match[2]
            referenced_column = foreign_key_match[3]
            on_delete = foreign_key_match[4]
            on_update = foreign_key_match[5]

            foreign_key_dict[constraint_name] = {
                'FOREIGN KEY': foreign_key_columns.strip('`'),
                'REFERENCE_TABLE': referenced_table,
                'REFERENCE_COL': referenced_column.strip('`'),
                'ON DELETE': on_delete.strip() if on_delete else '',
                'ON UPDATE': on_update.strip() if on_update else ''
            }

        if foreign_key_dict:
            current_attributes['CONSTRAINT_FOREIGN KEY'] = foreign_key_dict

        check_matches = re.findall(check_pattern, match[1])
        check_dict = {}
        for check_match in check_matches:
            constraint_name = check_match[0]
            check_condition = check_match[1]
            check_dict[constraint_name] = check_condition

        if check_dict:
            current_attributes['CONSTRAINT_CHECK'] = check_dict
            
        unique_key_matches = re.findall(unique_key_pattern, match[1])
        unique_key_dict = {}
        for unique_key_match in unique_key_matches:
            unique_key_name = unique_key_match[0]
            unique_key_columns = unique_key_match[1].split(',')
            unique_key_dict[unique_key_name] = [col.strip('`') for col in unique_key_columns]

        if unique_key_dict:
            current_attributes['UNIQUE KEY'] = unique_key_dict

        table_dict[current_table] = current_attributes

    return table_dict


def generate_single_foreign_key_sql(constraint_name, foreign_key):
    foreign_key_name = foreign_key['FOREIGN KEY']
    referenced_table = foreign_key['REFERENCE_TABLE']
    referenced_columns = foreign_key['REFERENCE_COL']
    on_delete = f"ON DELETE {foreign_key['ON DELETE']}" if foreign_key['ON DELETE'] else ""
    on_update = f"ON UPDATE {foreign_key['ON UPDATE']}" if foreign_key['ON UPDATE'] else ""
    foreign_key_sql = f"CONSTRAINT `{constraint_name}` FOREIGN KEY (`{foreign_key_name}`) REFERENCES `{referenced_table}` (`{referenced_columns}`) {on_delete} {on_update}"
    return foreign_key_sql


def check_primary_key_differences(table_name, attributes1, attributes2):
    sql_script = ""
    if 'PRIMARY KEY' in attributes1 and 'PRIMARY KEY' in attributes2:
        if attributes1['PRIMARY KEY'] != attributes2['PRIMARY KEY']:
            # Primary key changed in commit 2
            sql_script += f"ALTER TABLE `{table_name}` DROP PRIMARY KEY;\n"
            primary_key_columns = ", ".join(attributes2['PRIMARY KEY'])
            sql_script += f"ALTER TABLE `{table_name}` ADD PRIMARY KEY ({primary_key_columns});\n"
        # Primary key remains the same, no action needed

    elif 'PRIMARY KEY' in attributes1 and 'PRIMARY KEY' not in attributes2:
        # Primary key removed in commit 2
        sql_script += f"ALTER TABLE `{table_name}` DROP PRIMARY KEY;\n"

    elif 'PRIMARY KEY' not in attributes1 and 'PRIMARY KEY' in attributes2:
        # Primary key added in commit 2
        primary_key_columns = ", ".join(attributes2['PRIMARY KEY'])
        sql_script += f"ALTER TABLE `{table_name}` ADD PRIMARY KEY ({primary_key_columns});\n"

    return sql_script


def check_foreign_key_differences(table_name, attributes1, attributes2):
    sql_script = ""
    if 'CONSTRAINT_FOREIGN KEY' in attributes1 and 'CONSTRAINT_FOREIGN KEY' in attributes2:
        if attributes1['CONSTRAINT_FOREIGN KEY'] != attributes2['CONSTRAINT_FOREIGN KEY']:
            # Foreign key changed in commit 2
            foreign_keys_to_drop = set(attributes1['CONSTRAINT_FOREIGN KEY'].keys()) - set(
                attributes2['CONSTRAINT_FOREIGN KEY'].keys())
            for foreign_key_name in foreign_keys_to_drop:
                sql_script += f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{foreign_key_name}`;\n"

            foreign_keys_to_add = set(attributes2['CONSTRAINT_FOREIGN KEY'].keys()) - set(
                attributes1['CONSTRAINT_FOREIGN KEY'].keys())
            for constraint_name in foreign_keys_to_add:
                foreign_key = attributes2['CONSTRAINT_FOREIGN KEY'][constraint_name]
                foreign_key_sql = generate_single_foreign_key_sql(constraint_name, foreign_key)
                sql_script += f"ALTER TABLE `{table_name}` ADD {foreign_key_sql};\n"
        # Foreign key remains the same, no action needed

    elif 'CONSTRAINT_FOREIGN KEY' in attributes1 and 'CONSTRAINT_FOREIGN KEY' not in attributes2:
        # Foreign key removed in commit 2
        foreign_keys_to_drop = attributes1['CONSTRAINT_FOREIGN KEY'].keys()
        for foreign_key_name in foreign_keys_to_drop:
            sql_script += f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{foreign_key_name}`;\n"

    elif 'CONSTRAINT_FOREIGN KEY' not in attributes1 and 'CONSTRAINT_FOREIGN KEY' in attributes2:
        # Foreign key added in commit 2
        foreign_keys_to_add = attributes2['CONSTRAINT_FOREIGN KEY'].keys()
        for constraint_name in foreign_keys_to_add:
            foreign_key = attributes2['CONSTRAINT_FOREIGN KEY'][constraint_name]
            foreign_key_sql = generate_single_foreign_key_sql(constraint_name, foreign_key)
            sql_script += f"ALTER TABLE `{table_name}` ADD {foreign_key_sql};\n"

    return sql_script


def check_constraint_check_differences(table_name, attributes1, attributes2):
    sql_script = ""
    if 'CONSTRAINT_CHECK' in attributes1 and 'CONSTRAINT_CHECK' in attributes2:
        if attributes1['CONSTRAINT_CHECK'] != attributes2['CONSTRAINT_CHECK']:
            # CONSTRAINT_CHECK changed in commit 2
            constraint_checks_to_drop = set(attributes1['CONSTRAINT_CHECK'].keys()) - set(
                attributes2['CONSTRAINT_CHECK'].keys())
            for constraint_name in constraint_checks_to_drop:
                sql_script += f"ALTER TABLE `{table_name}` DROP CONSTRAINT `{constraint_name}`;\n"

            constraint_checks_to_add = set(attributes2['CONSTRAINT_CHECK'].keys()) - set(
                attributes1['CONSTRAINT_CHECK'].keys())
            for constraint_name in constraint_checks_to_add:
                constraint_check = attributes2['CONSTRAINT_CHECK'][constraint_name]
                attribute_str = f"CONSTRAINT `{constraint_name}` CHECK {constraint_check}"
                sql_script += f"ALTER TABLE `{table_name}` ADD {attribute_str};\n"
        # CONSTRAINT_CHECK remains the same, no action needed

    elif 'CONSTRAINT_CHECK' in attributes1 and 'CONSTRAINT_CHECK' not in attributes2:
        # CONSTRAINT_CHECK removed in commit 2
        constraint_checks_to_drop = attributes1['CONSTRAINT_CHECK'].keys()
        for constraint_name in constraint_checks_to_drop:
            sql_script += f"ALTER TABLE `{table_name}` DROP CONSTRAINT `{constraint_name}`;\n"

    elif 'CONSTRAINT_CHECK' not in attributes1 and 'CONSTRAINT_CHECK' in attributes2:
        # CONSTRAINT_CHECK added in commit 2
        constraint_checks_to_add = attributes2['CONSTRAINT_CHECK'].keys()
        for constraint_name in constraint_checks_to_add:
            constraint_check = attributes2['CONSTRAINT_CHECK'][constraint_name]
            attribute_str = f"CONSTRAINT `{constraint_name}` CHECK {constraint_check}"
            sql_script += f"ALTER TABLE `{table_name}` ADD {attribute_str};\n"

    return sql_script


def check_unique_key_differences(table_name, attributes1, attributes2):
    sql_script = ""
    if 'UNIQUE KEY' in attributes1 and 'UNIQUE KEY' in attributes2:
        if attributes1['UNIQUE KEY'] != attributes2['UNIQUE KEY']:
            # UNIQUE KEY changed in commit 2
            unique_keys_to_drop = set(attributes1['UNIQUE KEY'].keys()) - set(
                attributes2['UNIQUE KEY'].keys())
            for constraint_name in unique_keys_to_drop:
                sql_script += f"ALTER TABLE `{table_name}` DROP INDEX `{constraint_name}`;\n"

            unique_keys_to_add = set(attributes2['UNIQUE KEY'].keys()) - set(
                attributes1['UNIQUE KEY'].keys())
            for constraint_name in unique_keys_to_add:
                unique_key = attributes2['UNIQUE KEY'][constraint_name]
                columns = ", ".join([f"`{column}`" for column in unique_key])
                sql_script += f"ALTER TABLE `{table_name}` ADD CONSTRAINT UNIQUE `{constraint_name}` ({columns});\n"
        # UNIQUE KEY remains the same, no action needed

    elif 'UNIQUE KEY' in attributes1 and 'UNIQUE KEY' not in attributes2:
        # UNIQUE KEY removed in commit 2
        unique_keys_to_drop = attributes1['UNIQUE KEY'].keys()
        for constraint_name in unique_keys_to_drop:
            sql_script += f"ALTER TABLE `{table_name}` DROP INDEX `{constraint_name}`;\n"

    elif 'UNIQUE KEY' not in attributes1 and 'UNIQUE KEY' in attributes2:
        # UNIQUE KEY added in commit 2
        unique_keys_to_add = attributes2['UNIQUE KEY'].keys()
        for constraint_name in unique_keys_to_add:
            unique_key = attributes2['UNIQUE KEY'][constraint_name]
            columns = ", ".join([f"`{column}`" for column in unique_key])
            sql_script += f"ALTER TABLE `{table_name}` ADD CONSTRAINT `{constraint_name}` UNIQUE `{constraint_name}` ({columns});\n"

    return sql_script


def generate_sql_diff(commit1_dict, commit2_dict):
    sql_script = ""

    # Get the set of all table names from both commits
    all_tables = set(commit1_dict.keys()).union(commit2_dict.keys())
    constraint_keywords = {'PRIMARY KEY', 'CONSTRAINT_FOREIGN KEY', 'CONSTRAINT_CHECK', 'UNIQUE KEY'}

    # Compare table attributes for each table
    for table_name in all_tables:
        if table_name not in commit1_dict:
            # Table added in commit 2
            attributes2 = commit2_dict[table_name]
            attribute_list = []
            for name, definition in attributes2.items():
                if name not in constraint_keywords:
                    attribute_list.append(f"{name} {definition}")

            attribute_str = ", \n".join(attribute_list)

            # Add PRIMARY KEY and CONSTRAINT_FOREIGN KEY separately if present
            if 'PRIMARY KEY' in attributes2:
                primary_key_columns = ", ".join(attributes2['PRIMARY KEY'])
                attribute_str += f", \nPRIMARY KEY (`{primary_key_columns}`)"
                
            if 'UNIQUE KEY' in attributes2:
                unique_keys = attributes2['UNIQUE KEY']
                for constraint_name, unique_key in unique_keys.items():
                    columns = ", ".join([f"`{column}`" for column in unique_key])
                    attribute_str += f", \nUNIQUE KEY `{constraint_name}` ({columns})"

            if 'CONSTRAINT_FOREIGN KEY' in attributes2:
                foreign_keys = attributes2['CONSTRAINT_FOREIGN KEY']
                for constraint_name, foreign_key in foreign_keys.items():
                    foreign_key_sql = generate_single_foreign_key_sql(constraint_name, foreign_key)
                    attribute_str += f", \n{foreign_key_sql}"
                    
            if 'CONSTRAINT_CHECK' in attributes2:
                check_keys = attributes2['CONSTRAINT_CHECK']
                for constraint_name, check_key in check_keys.items():
                    attribute_str += f", \nCONSTRAINT `{constraint_name}` CHECK {check_key}"

            sql_script += f"CREATE TABLE `{table_name}` (\n{attribute_str});\n"
        elif table_name not in commit2_dict:
            # Table deleted in commit 2
            sql_script += f"DROP TABLE `{table_name}`;\n"
        else:
            attributes1 = commit1_dict[table_name]
            attributes2 = commit2_dict[table_name]

            # Compare attributes for the table
            for attribute_name, attribute_definition in attributes1.items():
                if attribute_name in constraint_keywords:
                    continue
                if attribute_name not in attributes2:
                    # Attribute deleted in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` DROP COLUMN `{attribute_name}`;\n"
                elif attribute_definition != attributes2[attribute_name]:
                    # Attribute changed in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` MODIFY COLUMN `{attribute_name}` {attributes2[attribute_name]};\n"

            # Check for new attributes added in commit 2
            for attribute_name, attribute_definition in attributes2.items():
                if attribute_name not in attributes1 and attribute_name not in constraint_keywords:
                    sql_script += f"ALTER TABLE `{table_name}` ADD COLUMN `{attribute_name}` {attribute_definition};\n"

            # Check for primary key differences
            sql_script += check_primary_key_differences(table_name, attributes1, attributes2)
            
            # Check for foreign key differences
            sql_script += check_foreign_key_differences(table_name, attributes1, attributes2)
            
            # Check for CONSTRAINT_CHECK differences
            sql_script += check_constraint_check_differences(table_name, attributes1, attributes2)

            # Check for UNIQUE KEY differences
            sql_script += check_unique_key_differences(table_name, attributes1, attributes2)

    return sql_script


def get_diff(commit1, commit2):
    commit1_dict = parse_sql_script(commit1)
    commit2_dict = parse_sql_script(commit2)
    return generate_sql_diff(commit1_dict, commit2_dict)