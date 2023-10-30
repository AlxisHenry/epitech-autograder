import { Client, Events, GatewayIntentBits } from 'discord.js';
import config from './config.json' assert { type: "json" };
import fs from 'fs/promises';
import { exec } from 'child_process';

const gifs = [
	"https://tenor.com/view/pig-windmill-gif-9413764",
	"https://tenor.com/view/spin-slap-windmill-gif-12199610",
	"https://tenor.com/view/christine-rock-climbing-top-rope-cool-wink-gif-13849776"
];
const DELAY = 45 * 60 * 1000; // 45 minutes

const { token } = config;
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const formatDate = (date, time) => {
	let fdate = new Date(`${date?.year}-${date?.month}-${date?.day}T${time?.hour}:${time?.minute}:00`);
	return fdate;
}

client.once(Events.ClientReady, async c => {
	console.log(`Logged in as ${c.user.tag}!`);

	let { course, date, time } = await loadAutograderData();

	client.user.setActivity(`Grading ${course}`);
	let current = formatDate(date, time);

	setInterval(async () => {
		await loadAutograderData(true)
	// }, DELAY / 2);
	}, 20000);
	
	setInterval(async () => {
		let { course, date, time } = await loadAutograderData();
		console.log(date, time, `Date has changed: ${current.getTime() !== formatDate(date, time).getTime()}`);
		let fdate = formatDate(date, time);
		if (current.getTime() !== fdate.getTime()) {
			console.log('Sending message to channel');
			client.channels.fetch('1168562165482012692').then(channel => {
				channel.send(`@everyone **${course}** is now being graded !\n`);
				channel.send(gifs[Math.floor(Math.random() * gifs.length)]);
			})
			current = fdate;
		}
	}, 40000);
});

async function loadAutograderData(run = false) {
	try {
		if (run) {
			console.log('Running autograder python script.');
			exec('python3 ./bot/main.py');
		}
		let data = await fs.readFile('./bot/autograder.json', 'utf8');
		return JSON.parse(data);
	} catch (error) {
		console.error('Error reading autograder data:', error);
		return {};
	}
}

client.login(token);