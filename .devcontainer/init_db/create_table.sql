CREATE TABLE employee_list(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    first_name VARCHAR(255) NOT NULL COMMENT 'First Name',
    surname VARCHAR(255) COMMENT 'Surname',
    position TINYINT NOT NULL COMMENT 'Position (0: Employee, 1: Manager, 2: Director)',
    department TINYINT NOT NULL COMMENT 'Department (0: HR, 1: IT, 2: Sales)',
    phone_number VARCHAR(20) NOT NULL COMMENT 'Phone Number',
    email VARCHAR(255) NOT NULL COMMENT 'Email Address',
    birth_date DATETIME COMMENT 'Birth Date',
    status TINYINT NOT NULL COMMENT 'Status (0: Inactive, 1: Active)',
    description VARCHAR(255) COMMENT 'Description',
    register_time DATETIME COMMENT 'Register Time',
    INDEX idx_employee_list_position (position) COMMENT 'Index for Position',
    INDEX idx_employee_list_department (department) COMMENT 'Index for Department',
    INDEX idx_employee_list_status (status) COMMENT 'Index for Status'
) COMMENT 'Employee Information for Management';

CREATE TABLE document_approval (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    issuer INT NOT NULL COMMENT 'Employee ID of the issuer (Who wants to take a day off)',
    assignee INT NOT NULL COMMENT 'Employee ID of the assignee (Who checks the request)',
    status TINYINT NOT NULL COMMENT 'Approval Status (0: Pending, 1: Approved, 2: Rejected)',
    dayoff_start_date DATE NOT NULL COMMENT 'Start date of requested day off',
    dayoff_end_date DATE NOT NULL COMMENT 'End date of requested day off',
    reason VARCHAR(255) COMMENT 'Reason for day off',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation timestamp',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update timestamp',
    FOREIGN KEY (issuer) REFERENCES employee_list(id)
) COMMENT 'Document approval for dayoff requests';
