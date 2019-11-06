module.exports = {
	port: '8655',
	knex: {
		client: 'pg',
		connection: {
			user: "music_festival",
            password: "p@ssw0rd",
            host: "localhost",
            port: "15432",
            database: 'music_festival'
		},
		useNullAsDefault: true
	},
	defaultItems: [
		{name: 'beer', quantity: 110},
		{name: 'koozies', quantity: 103},
		{name: 'openers', quantity: 9}
	]
}
