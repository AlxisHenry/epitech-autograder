import { Client, Events, GatewayIntentBits } from 'discord.js';
import config from './config.json' assert { type: "json" };
import fs from 'fs/promises';
import { exec } from 'child_process';

const gifs = [
	"https://tenor.com/view/pig-windmill-gif-9413764",
	"https://tenor.com/view/spin-slap-windmill-gif-12199610",
	"https://tenor.com/view/christine-rock-climbing-top-rope-cool-wink-gif-13849776"
];
const botChannel = '1168562165482012692';
const DELAY = 1 * 60 * 1000; // every minute

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

	console.log('Starting autograder loop. Checking every', DELAY / 1000, 'seconds.');
	console.log(`Retrieved data: ${course} ${date?.year}-${date?.month}-${date?.day}T${time?.hour}:${time?.minute}:00`)

	setInterval(async () => {
		console.log('Running autograder python script.');
		await loadAutograderData(true)
	}, DELAY / 2);
	
	setInterval(async () => {
		let { course, date, time } = await loadAutograderData();
		console.log(date, time, `Date has changed: ${current.getTime() !== formatDate(date, time).getTime()}`);
		let fdate = formatDate(date, time);
		if (current.getTime() !== fdate.getTime()) {
			console.log('Sending message to channel');
			client.channels.fetch(botChannel).then(channel => {
				channel.send(`@everyone **${course}** is now being graded !`);
				channel.send(gifs[Math.floor(Math.random() * gifs.length)]);
			})
			current = fdate;
		}
	}, DELAY);
});

async function loadAutograderData(run = false) {
	try {
		if (run) {
			exec('python3 ./bot/main.py', (error, stdout, stderr) => {
				if (error) {
					console.error(`exec error: ${error}`);
					return;
				}
				console.log(`stdout: ${stdout}`);
				console.error(`stderr: ${stderr}`);
			});
		}
		let data = await fs.readFile('./bot/autograder.json', 'utf8');
		return JSON.parse(data);
	} catch (error) {
		console.error('Error reading autograder data:', error);
		return {};
	}
}

client.login(token);