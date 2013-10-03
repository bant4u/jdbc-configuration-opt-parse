from optparse import OptionParser
from fabric.api import *

def main():
    usage = "useage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("--datasource", type="string", dest="datasource",default=None, help="Put data source name or Ex. java:jboss/datasources/LiferayPool ")
    parser.add_option("--url",type="string",dest="connection",default=None,help="Put url of Database RDS")
    parser.add_option("--jndi",type="string",dest="jndi",default=None,help="Name of jndi")
    parser.add_option("--database", type="string", dest="database",default=None, help="Ex. name of database you want to connect db_sbw")
    parser.add_option("--username", type="string", dest="username",default=None,help="Username Ex. SBW")
    parser.add_option("--password",type="string",dest="password",default=None,help="Refer vault password for security")
    parser.add_option("--drivername",type="string", dest="drivername",default=None, help="Ex. true or false")
    parser.add_option("--remove", type="string", dest="remove",default=True, help="Ex. Yes or No")
    parser.add_option("--update", type="string", dest="update",default=True, help="Ex. Yes or No")
    parser.add_option("--add", type="string", dest="add",default=True,help="Ex. Yes or No")
    (options, args) = parser.parse_args()
    connection=options.connection
    print connection
    database=options.database
    print database
    connectionurl=str(connection)+':3306/'+str(database)
    print connectionurl

    #Adding New Datasources
    if (options.add=="Yes"):
        with lcd('$JBOSS_HOME/bin'):
            command = "./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:add(jndi-name=%s,connection-url=%s,user-name=%s,password=%s,driver-name=%s)'"
            print "Adding new datasource............."
            addcommand = command % (options.datasource,options.jndi,connectionurl,options.username,options.password,options.drivername)
            local(addcommand)
            print "Successfully Added!!!"

    if (options.remove=="Yes"):
        with lcd('$JBOSS_HOME/bin'):
            print "removing...."
            command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:remove'"
            removecommand= command % options.datasource
            local(removecommand)

    if (options.update=="Yes"):
        with lcd('$JBOSS_HOME/bin'):
            connectionname="connection-url"
            username="user-name"
            password="password"
            print "helo"
            print options.connection
            print "Helo"
            if(options.connection!=None and options.database!=None and options.username!=None and options.password!=None):
                print "All"
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,connectionname,connectionurl)
                local(updatecommand)
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,username,options.username)
                local(updatecommand)
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,password,options.password)
                local(updatecommand)

            elif(options.connection!=None and options.database!=None):
                print "Connection"
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,connectionname,connectionurl)
                local(updatecommand)

            elif(options.username!=None and options.password!=None):
                print "Username and pass1"
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,username,options.username)
                local(updatecommand)
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,password,options.password)
                local(updatecommand)


            elif(options.username!=None):
                print "username"
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,username,options.username)
                local(updatecommand)

            elif(options.password!=None):
                print "Password"
                command="./jboss-cli.sh --connect '/subsystem=datasources/data-source=%s:write-attribute(name=%s,value=%s)'"
                updatecommand= command % (options.datasource,password,options.password)
                local(updatecommand)
            else:
                print "Wrong commands"


if __name__ == "__main__":
    main()

