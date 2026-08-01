"""
Matterbridge: Open-source chat bridge for multiple messaging platforms

Key features:
- Bridges multiple chat protocols/platforms
- Supports message edits, deletes, threading, attachments
- Username/avatar spoofing, private groups
- API for third-party integrations

Natively supported platforms:
Discord, Gitter, IRC, Matrix, Mattermost, Slack, Telegram, WhatsApp, XMPP, etc.

Third-party integrations via API:
Minecraft, Reddit, Facebook Messenger, etc.

Installation:
- Pre-built binaries available
- Can be built from source (Go 1.18+)
- Docker and package manager options

Configuration:
- TOML config file
- Supports multiple gateways/bridges
- Flexible message formatting options

Usage:
./matterbridge -conf config.toml

Key benefits:
- Unifies communication across disparate platforms
- Open-source and self-hostable
- Actively maintained with regular updates

Limitations:
- Some platforms require separate builds (e.g. WhatsApp multi-device)
- Setup can be complex for multiple bridges

Matterbridge can be build without gcc/c-compiler: If you're running on windows first run set CGO_ENABLED=0 on other platforms you prepend CGO_ENABLED=0 to the go build command. (eg CGO_ENABLED=0 go install github.com/42wim/matterbridge)

To install the latest stable run:

go install github.com/42wim/matterbridge
To install the latest dev run:

go install github.com/42wim/matterbridge@master
To install the latest stable run without msteams or zulip bridge:

go install -tags nomsteams,nozulip github.com/42wim/matterbridge
You should now have matterbridge binary in the ~/go/bin directory:

$ ls ~/go/bin/
matterbridge
Building with whatsapp (beta) multidevice support
Because the library we use for Whatsapp multidevice support includes a GPL3 library we can not provide you binaries. (as this would require the Matterbridge to change it license to GPL)

Matterbridge can be build without gcc/c-compiler: If you're running on windows first run set CGO_ENABLED=0 on other platforms you prepend CGO_ENABLED=0 to the go build command. (eg CGO_ENABLED=0 go install github.com/42wim/matterbridge)

So this means you have to build it yourself using the instructions below:

go install -tags whatsappmulti github.com/42wim/matterbridge@master
If you're low on memory and don't need msteams:

go install -tags nomsteams,whatsappmulti github.com/42wim/matterbridge@master
You should now have matterbridge binary in the ~/go/bin directory:

$ ls ~/go/bin/
matterbridge
Configuration
Basic configuration
See howto for a step by step walkthrough for creating your configuration.

Settings
All possible settings for each bridge.

Advanced configuration
matterbridge.toml.sample for documentation and an example.
Examples
Bridge mattermost (off-topic) - irc (#testing)
[irc]
    [irc.libera]
    Server="irc.libera.chat:6667"
    Nick="yourbotname"

[mattermost]
    [mattermost.work]
    Server="yourmattermostserver.tld"
    Team="yourteam"
    Login="yourlogin"
    Password="yourpass"
    PrefixMessagesWithNick=true
    RemoteNickFormat="[{PROTOCOL}] <{NICK}> "

[[gateway]]
name="mygateway"
enable=true
    [[gateway.inout]]
    account="irc.libera"
    channel="#testing"

    [[gateway.inout]]
    account="mattermost.work"
    channel="off-topic"
Bridge slack (#general) - discord (general)
[slack]
[slack.test]
Token="yourslacktoken"
PrefixMessagesWithNick=true

[discord]
[discord.test]
Token="yourdiscordtoken"
Server="yourdiscordservername"

[general]
RemoteNickFormat="[{PROTOCOL}/{BRIDGE}] <{NICK}> "

[[gateway]]
    name = "mygateway"
    enable=true

    [[gateway.inout]]
    account = "discord.test"
    channel="general"

    [[gateway.inout]]
    account ="slack.test"
    channel = "general"
Running
See howto for a step by step walkthrough for creating your configuration.

Usage of ./matterbridge:
  -conf string
        config file (default "matterbridge.toml")
  -debug
        enable debug
  -gops
        enable gops agent
  -version
        show version
Docker
Please take a look at the Docker Wiki page for more information.

Systemd
Please take a look at the Service Files page for more information.

Changelog
See changelog.md

FAQ
See FAQ

Related projects
jwflory/ansible-role-matterbridge (Ansible role to simplify deploying Matterbridge)
matterbridge autoconfig
matterbridge config viewer
matterbridge-heroku
mattereddit
matterlink
mattermost-plugin - Run matterbridge as a plugin in mattermost
pyCord (crossplatform chatbot)
fbridge (Facebook messenger support)
isla (Bot for Discord-Telegram groups used alongside matterbridge)
matterbabble (Connect Discourse threads to Matterbridge)
nextcloud talk (Integrates matterbridge in Nextcloud Talk)
mattercraft (Minecraft bridge)
vs-matterbridge (Vintage Story bridge)
ServUO-matterbridge (A matterbridge connector for ServUO servers)
ts-matterbridge (Integrate teamspeak chat with matterbridge)
Articles / Tutorials
matterbridge on kubernetes
https://mattermost.com/blog/connect-irc-to-mattermost/
https://blog.valvin.fr/2016/09/17/mattermost-et-un-channel-irc-cest-possible/
https://blog.brightscout.com/top-10-mattermost-integrations/
https://www.algoo.fr/blog/2018/01/19/recouvrez-votre-liberte-en-quittant-slack-pour-un-mattermost-auto-heberge/
https://kopano.com/blog/matterbridge-bridging-mattermost-chat/
https://www.stitcher.com/s/?eid=52382713
https://daniele.tech/2019/02/how-to-use-matterbridge-to-connect-2-different-slack-workspaces/
https://userlinux.net/mattermost-and-matterbridge.html
https://nextcloud.com/blog/bridging-chat-services-in-talk/
https://minecraftchest1.wordpress.com/2021/06/05/how-to-install-and-setup-matterbridge/
Youtube: whatsapp - telegram bridging
Thanks
This project is supported by:



Matterbridge wouldn't exist without these libraries:

discord - https://github.com/bwmarrin/discordgo
echo - https://github.com/labstack/echo
gops - https://github.com/google/gops
gozulipbot - https://github.com/ifo/gozulipbot
gumble - https://github.com/layeh/gumble
harmony - https://github.com/harmony-development/shibshib
irc - https://github.com/lrstanley/girc
keybase - https://github.com/keybase/go-keybase-chat-bot
matrix - https://github.com/matrix-org/gomatrix
mattermost - https://github.com/mattermost/mattermost-server
msgraph.go - https://github.com/yaegashi/msgraph.go
mumble - https://github.com/layeh/gumble
nctalk - https://github.com/gary-kim/go-nc-talk
rocketchat - https://github.com/RocketChat/Rocket.Chat.Go.SDK
slack - https://github.com/nlopes/slack
sshchat - https://github.com/shazow/ssh-chat
steam - https://github.com/Philipp15b/go-steam
telegram - https://github.com/go-telegram-bot-api/telegram-bot-api
tengo - https://github.com/d5/tengo
vk - https://github.com/SevereCloud/vksdk
whatsapp - https://github.com/Rhymen/go-whatsapp
whatsapp - https://github.com/tulir/whatsmeow
xmpp - https://github.com/mattn/go-xmpp
zulip - https://github.com/ifo/gozulipbot
"""
