\# TeleForge: Automated Group Provisioning Bot



A Python-based Telegram automation tool that allows authorized users to create groups on demand. The bot automatically generates invite links and notifies team members, overcoming common API privacy restrictions.



\## 🚀 Features

\- \*\*On-Demand Group Creation\*\*: Use `/creategroup <name>` to spin up a new group instantly.

\- \*\*Auto-Invite Link\*\*: Generates a permanent invite link for every new group.

\- \*\*Smart Notification\*\*: Sends the invite link via DM to specified team members (@prakhargupta, @edrianzeropenny).

\- \*\*Access Control\*\*: Only the authorized user ID can trigger the bot.

\- \*\*Privacy Compliant\*\*: Designed to work even if target users have "Add to Group" privacy restrictions.



\## 🛠 Setup \& Installation



\### 1. Requirements

\- Python 3.8+

\- Telegram `API\_ID` and `API\_HASH` (obtain from \[my.telegram.org](https://my.telegram.org))



\### 2. Environment Variables

Create a `.env` file in the root directory:

```text

API\_ID=1234567

API\_HASH=your\_api\_hash\_here

AUTHORIZED\_USER\_ID=your\_numeric\_id\_here

