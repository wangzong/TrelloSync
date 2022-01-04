import asana

personal_access_token = "1/1201328974010558:2933f7683268749efc77bc36269e0475"

# Construct an Asana client
client = asana.Client.access_token(personal_access_token)
# Set things up to send the name of this script to us to show that you succeeded! This is optional.
client.options['client_name'] = "hello_world_python"

# Get your user info
me = client.users.me()

# Print out your information
print("Hello world! " + "My name is " + me['name'] + "!")

result = client.tasks.create_task({'field': 'value', 'field': 'value'}, opt_pretty=True)