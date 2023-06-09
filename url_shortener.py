{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f444e007",
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, jsonify, request, redirect\n",
    "import random\n",
    "import string\n",
    "import validators\n",
    "import datetime\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Dictionary to store the URL mappings\n",
    "url_map = {}\n",
    "\n",
    "# Generate a random fixed-size string of alphanumeric characters\n",
    "def generate_random_string(size=8):\n",
    "    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))\n",
    "\n",
    "# Create a new shortened URL with a random name\n",
    "@app.route('/url', methods=['POST'])\n",
    "def create_short_url():\n",
    "    url = request.json.get('url')\n",
    "    if not url or not validators.url(url) or len(url) > 250:\n",
    "        return jsonify({'error': 'Invalid URL or URL length > 250 characters.'}), 400\n",
    "    short_name = generate_random_string()\n",
    "    while short_name in url_map:\n",
    "        short_name = generate_random_string()\n",
    "    url_map[short_name] = {'url': url, 'created': datetime.datetime.utcnow()}\n",
    "    return jsonify({'short_url': f'/url/{short_name}'}), 201\n",
    "\n",
    "# Create a new shortened URL with a custom name (for premium clients)\n",
    "@app.route('/url/<custom_name>', methods=['POST'])\n",
    "def create_custom_short_url(custom_name):\n",
    "    url = request.json.get('url')\n",
    "    if not url or not validators.url(url) or len(url) > 250:\n",
    "        return jsonify({'error': 'Invalid URL or URL length > 250 characters.'}), 400\n",
    "    if custom_name in url_map:\n",
    "        return jsonify({'error': 'Custom name already taken.'}), 400\n",
    "    url_map[custom_name] = {'url': url, 'created': datetime.datetime.utcnow()}\n",
    "    return jsonify({'short_url': f'/url/{custom_name}'}), 201\n",
    "\n",
    "# Redirect to the original URL for a given short name\n",
    "@app.route('/url/<short_name>', methods=['GET'])\n",
    "def get_original_url(short_name):\n",
    "    if short_name not in url_map:\n",
    "        return jsonify({'error': 'Short URL not found.'}), 404\n",
    "    url_map[short_name]['accessed'] = url_map[short_name].get('accessed', 0) + 1\n",
    "    return redirect(url_map[short_name]['url'], code=302)\n",
    "\n",
    "# Optional: count how many times a URL was accessed\n",
    "@app.route('/url/<short_name>/stats', methods=['GET'])\n",
    "def get_url_stats(short_name):\n",
    "    if short_name not in url_map:\n",
    "        return jsonify({'error': 'Short URL not found.'}), 404\n",
    "    accessed = url_map[short_name].get('accessed', 0)\n",
    "    return jsonify({'accessed': accessed}), 200\n",
    "\n",
    "# Optional: automatically delete URLs older than 30 days\n",
    "@app.before_request\n",
    "def delete_expired_urls():\n",
    "    now = datetime.datetime.utcnow()\n",
    "    for short_name, data in url_map.copy().items():\n",
    "        created = data.get('created')\n",
    "        if created and (now - created).days >= 30:\n",
    "            del url_map[short_name]\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
