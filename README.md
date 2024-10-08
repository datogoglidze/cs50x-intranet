# Intranet | cs50x
The project "Intranet" is about managing company-wide communications between employees and administrators.

* Employees can create statements, for example, statements about requesting paid vacation, and save them for administrators to review. Administrators can view the statements and make decisions on approving or rejecting them.
* Administrator can post news for employees, and they can view it.
* It has workspace, where employees can access links to all necessary tools, that can be important for their work.

<be>
<br>

> [!IMPORTANT]
> **How to run the project using Docker (Execute following commands in bash)**
> * "make intranet-network";
> * "make db";
> * connect to the MsSQL server, execute `create database Intranet` and run sql scripts located in `intranet/mssql/scripts/` on Intranet database;
> * "make up".
