import os
import json

THREADS_DIR = os.path.join(os.path.dirname(__file__), '../data/threads')

def load_history(thread_id):
	"""
	Load message history for a given thread ID.
	Returns a list of dicts with only role, text, and timestamp for each message.
	"""
	thread_path = os.path.join(THREADS_DIR, f"{thread_id}.json")
	if not os.path.exists(thread_path):
		return []
	with open(thread_path, 'r', encoding='utf-8') as f:
		data = json.load(f)
	messages = data.get('messages', [])
	history = []
	for msg in messages:
		history.append({
			'role': msg.get('role'),
			'text': msg.get('text'),
			'timestamp': msg.get('timestamp')
		})
	return history
