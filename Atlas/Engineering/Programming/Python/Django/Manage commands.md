`startap myapp` - create application named `myapp`
`shell` - open Python REPL in the project context
`createsuperuser` create an admin super user
`runserver` - run dev server

### Migrations

`makemigrations name` - create a new SQL migration based on model file
`sqlmigrate blog 001` - open a SQL migration blog number 001
`migrate` - apply migrations
`dumpdata --indent=2 --output=mysite_data.json` - export data from a database
`loaddata mysite_data.json` - import data into database
