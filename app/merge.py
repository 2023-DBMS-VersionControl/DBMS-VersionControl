from diff import read_sql_file ,parse_sql_script, generate_attribute_string, generate_sql_diff, get_diff
import mysql.connector
import uuid
import datetime
import time
import globals
from commit import commit


# Add branch format for sql script in different branch
def branch_format(branch_list, branch_name):
    if branch_list[0].startswith(", \n"):
        branch_list[0] = branch_list[0][3:]
    
    branch_list.insert(0, f"/* {branch_name} */")
    branch_list.append("/************/\n")
    
    sql_script = '\n'.join(branch_list)
    return sql_script

# Generate attribute string for column definition
def check_table_conflicts(is_conflict, table_name, branch1_name, table1, branch2_name, table2):
    sql_script = ""
    attribute_str = ""
    nonconflict_attr_dict = {}

    # Change the order of two_tables
    two_tables = set(table1.keys()).union(table2.keys())
    constraint_keywords = ['PRIMARY KEY', 'CONSTRAINT_FOREIGN KEY', 'UNIQUE KEY', 'CONSTRAINT_CHECK']
    
    two_tables_without_keywords = set(table1.keys()).union(table2.keys())
    for keyword in constraint_keywords:
        two_tables_without_keywords.discard(keyword)
    
    two_tables_with_keywords = two_tables.difference(two_tables_without_keywords)
    two_tables_in_order = list(two_tables_without_keywords) + list(two_tables_with_keywords)

    # Check conflicts in column definitions
    for column_name in two_tables_in_order:
        # Column created
        if column_name not in table1:
            nonconflict_attr_dict.update({column_name: table2[column_name]})
        # Column deleted
        elif column_name not in table2:
            is_conflict = True
            attribute_str += branch_format([generate_attribute_string({column_name: table1[column_name]})], branch1_name)
            attribute_str += branch_format([''], branch2_name)
        # Column exists in both tables, check for conflicts
        else:
            # Column updated
            if table1[column_name] != table2[column_name]:
                is_conflict = True
                attribute_str += branch_format([generate_attribute_string({column_name: table1[column_name]})], branch1_name)
                attribute_str += branch_format([generate_attribute_string({column_name: table2[column_name]})], branch2_name)
            # Column remains the same
            else:
                nonconflict_attr_dict.update({column_name: table1[column_name]})
                
    if attribute_str:
        attribute_str = generate_attribute_string(nonconflict_attr_dict) +',\n'+ attribute_str
    else:
        attribute_str = generate_attribute_string(nonconflict_attr_dict)
    # sql_script += f"DROP TABLE IF EXISTS `{table_name}`;\n"
    sql_script += f"CREATE TABLE `{table_name}` (\n{attribute_str});\n"
    return is_conflict, sql_script


# Check if there in any conflict when merging different branches
def check_branch_conflicts(branch1_name, branch1, branch2_name, branch2):
    is_conflict = False
    sql_script = ""
    all_tables = set(branch1.keys()).union(branch2.keys())
    
    # Check table conflicts
    for table_name in all_tables:
        # Table created
        if table_name not in branch1.keys():
            sql_script += generate_sql_diff({}, {table_name: branch2[table_name]})
            
        # Table deleted
        elif table_name not in branch2.keys():
            sql_script += branch_format([generate_sql_diff({}, {table_name: branch1[table_name]})], branch1_name)
            sql_script += branch_format([''], branch2_name)
            is_conflict = True
        
        # Table updated -> Check conflicts in table definitions
        else:
            if branch1[table_name] == branch2[table_name]:
                sql_script += generate_sql_diff({}, {table_name: branch1[table_name]})
            else:
                table_conflict = check_table_conflicts(is_conflict, table_name, branch1_name, branch1[table_name], branch2_name, branch2[table_name])
                is_conflict = table_conflict[0]
                sql_script += table_conflict[1]
        
    return is_conflict, sql_script


def merge_schema(commit1_dict, commit2_dict):
    merged_schema = {}

    # Merge tables from commit1
    for table_name, schema in commit1_dict.items():
        merged_schema[table_name] = schema

    # Merge tables from commit2
    for table_name, schema in commit2_dict.items():
        if table_name in merged_schema:
            # Table already exists, merge the schema
            merged_schema[table_name].update(schema)
        else:
            # Table doesn't exist, add it to the merged commit
            merged_schema[table_name] = schema

    return merged_schema

def insert_into_merge_table(merged_version, main_tail_version, target_tail_version):
    insert = "INSERT INTO merge (merged_version, main_branch_version, target_branch_version) VALUES (%s, %s, %s)"
    val = (merged_version, main_tail_version, target_tail_version)
    globals.vc_cursor.execute(insert, val)
    globals.vc_connect.commit()
    return 

# Merge two branches by merged_schema_dict and main_schema_dict
def merge_by_merged_dict(main_branch_name, main_tail_version, target_branch_name, target_tail_version, merged_schema_dict):
    is_merged = False
    # Turn merged schema into sql script
    merged_sql_script = generate_sql_diff({}, merged_schema_dict)

    # Update userdb
    update_result = update_userdb_schema(main_branch_name, merged_sql_script)

    # Successfully update userdb
    if update_result[0]:
        # Call commit(msg) and get version number
        msg = f"Merge {target_branch_name} into {main_branch_name}"
        merged_version = commit(msg)
        if merged_version:
            # Insert into merge table
            insert_into_merge_table(merged_version, main_tail_version, target_tail_version)
            return update_result[0], msg
        else:
            return False, "Failed to commit!"
    # Failed to update userdb
    else:
        return update_result


    """
    # Merged schema
    downgrade = generate_sql_diff(main_schema_dict, merged_schema_dict)
    upgrade = generate_sql_diff(merged_schema_dict, main_schema_dict)

    # msg = f"Merge {target_branch_name} into {main_branch_name}"
    merged_version = str(uuid.uuid4())[:8]

    # Get branch info
    query = f"SELECT * FROM branch WHERE tail = '{main_tail_version}'"
    globals.vc_cursor.execute(query)
    main_branch_info = globals.vc_cursor.fetchall()[0]
    if not main_branch_info:
        return is_merged, "No such branch with this tail version!"
    last_version = main_branch_info[2]
    main_branch_id = main_branch_info[0]
    msg = f"Merge {target_tail_version} into {main_tail_version}"


    #### 只留merge table 其他call commit->要拿最新版

    # Insert into commit table
    insert = "INSERT INTO commit (version, bid, last_version, upgrade, downgrade, time, uid, msg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (merged_version, main_branch_id, last_version, upgrade, downgrade, datetime.datetime.now(), globals.current_uid, msg)
    globals.vc_cursor.execute(insert, val)

    # Update branch table
    update = "UPDATE branch SET tail = %s WHERE bid = %s;"
    val = (merged_version, main_branch_id)
    globals.vc_cursor.execute(update, val)

    # Insert into merge table
    insert = "INSERT INTO merge (merged_version, main_branch_version, target_branch_version) VALUES (%s, %s, %s)"
    val = (merged_version, main_tail_version, target_tail_version)
    globals.vc_cursor.execute(insert, val)

    # Update user table
    update = "UPDATE user SET current_version = %s, current_bid = %s WHERE uid = %s;"
    val = (merged_version, main_branch_id, globals.current_uid)
    globals.vc_cursor.execute(update, val)

    globals.vc_connect.commit()
    """
    print(f"Successfully merged {target_tail_version} into {main_tail_version}!")
    is_merged = True
    return is_merged, f"Successfully merged {target_tail_version} into {main_tail_version}!"
    

def get_branch_tail_version(branch_name):
    query = "SELECT name, tail FROM branch WHERE name = (%s);"
    globals.vc_cursor.execute(query, (branch_name, ))
    branch_existed = globals.vc_cursor.fetchall()
    if not branch_existed:
        return None
    else:
        return branch_existed[0][1]

"""
Check if 2 branches can be merged
Y: Branches merged  -> error???
N: Return conflict sql script
"""
def merge(main_branch_name, target_branch_name):
    is_merged = False

    # Check if 2 branches exist
    main_tail_version = get_branch_tail_version(main_branch_name)
    if main_tail_version is None:
        return is_merged, f"Branch {main_branch_name} does not exist."
    
    target_tail_version = get_branch_tail_version(target_branch_name)
    if target_tail_version is None:
        return is_merged, f"Branch {target_branch_name} does not exist."

    # Read main branch tail and target branch tail sql file
    main_branch_path = f"./branch_tail_schema/{main_branch_name}.sql"
    target_branch_path = f"./branch_tail_schema/{target_branch_name}.sql"
    main_schema = read_sql_file(main_branch_path)
    target_schema = read_sql_file(target_branch_path)
    # Parse sql scripts into dictionary
    main_schema_dict = parse_sql_script(main_schema)
    target_schema_dict = parse_sql_script(target_schema)

    # Check if there is any conflict between 2 branches
    is_conflict = check_branch_conflicts(main_branch_name, main_schema_dict, target_branch_name, target_schema_dict)
    # if conflict exists: show conflicts
    if is_conflict[0]:
        print("Schema conflict exists between 2 branches as follows:")
        conflict_sql_script = is_conflict[1]
        print(conflict_sql_script)
        return is_merged, conflict_sql_script
    # if there is no conflict: merge 2 branches
    else:
        merged_schema_dict = merge_schema(main_schema_dict, target_schema_dict)
        result = merge_by_merged_dict(main_branch_name, main_tail_version, target_branch_name, target_tail_version, merged_schema_dict)
        return result


def sql_script_into_list(sql_script):
    sql_script_list = sql_script.split(";")
    sql_script_list.pop()
    for i in range(len(sql_script_list)):
        sql_script_list[i] = sql_script_list[i]+";"
    return sql_script_list

def update_userdb_schema(main_branch_name, sql_script):
    # Drop all tables
    globals.user_cursor.execute("SHOW Tables") 
    existed_tables = globals.user_cursor.fetchall()
    try:
        for table in existed_tables:
            globals.user_cursor.execute(f"DROP TABLE {table[0]};")
        globals.user_connect.commit()
    except Exception as e:
        return False, f"When updating userdb schema, drop all tables failed.\nError: {e} "
    
    # Execute fixed sql script
    fixed_sql_script_list = sql_script_into_list(sql_script)
    globals.user_cursor.execute("SET foreign_key_checks = 0;")
    for script in fixed_sql_script_list:
        if script:
            try:
                globals.user_cursor.execute(script)
                globals.user_connect.commit()
            except Exception as e:
                # Create original schema
                main_branch_tail_schema = read_sql_file(f"./branch_tail_schema/{main_branch_name}.sql")
                globals.user_cursor.execute(main_branch_tail_schema)
                return False, f"Error: {e}", sql_script
    globals.user_cursor.execute("SET foreign_key_checks = 1;")
    return True, "Successfully updated userdb schema!"


"""
Merge 2 branches after conflict fixed
"""
def merge_after_conflict_fixed(main_branch_name, target_branch_name, fixed_sql_script):
    is_merged = False

    # Check if 2 branches exist
    main_tail_version = get_branch_tail_version(main_branch_name)
    if main_tail_version is None:
        return is_merged, f"Branch {main_branch_name} does not exist." 
    target_tail_version = get_branch_tail_version(target_branch_name)
    if target_tail_version is None:
        return is_merged, f"Branch {target_branch_name} does not exist."

    # Execute fixed sql script
    update_result = update_userdb_schema(main_branch_name, fixed_sql_script)

    # Successfully update userdb schema, return success message
    if update_result[0]:
        print(update_result[1])
        # Call commit()
        msg = f"Merge {target_branch_name} into {main_branch_name} after conflict fixed"
        merged_version = commit(msg)

        # Insert merge info into merge table
        insert_into_merge_table(merged_version, main_tail_version, target_tail_version)
        is_merged = True
        return is_merged, msg
    # else failed to update userdb schema, return error message
    else:
        return is_merged, update_result[1], update_result[2]

# TEST
if __name__ == '__main__':
    # merge('branch1', 'branch2')
    fixed_sql_script = """

CREATE TABLE `course` (
  `Id` varchar(10) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `TeacherID` varchar(20) NOT NULL,
  KEY fk_teach (`TeacherID`),
  CONSTRAINT fk_teach FOREIGN KEY (`TeacherID`) REFERENCES teacher (`Id`)
 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int(11) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Gender` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Gender` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


"""
    print(f"merge_after_conflict_fixed: {merge_after_conflict_fixed('branch1', 'branch2', fixed_sql_script)}")