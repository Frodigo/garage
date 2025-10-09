---
date: 2025-10-17
title: Omarchy review after a month of using
permalink: omarchy-review-after-a-month-of-using
---
A month ago, I became the owner of a *Framework* Laptop 12 and needed to install an operating system on it. I chose Omarchy, and in this article I wanted to describe my experiences with it over the past few weeks.

## Why Omarchy

On my desktop computer, I use Pop OS, and on my company computer, *Ubuntu*. Initially, I also wanted to install Ubuntu on my new laptop so I could have a similar system everywhere. I learned about Omarchy by accident. A friend sent me a [YouTube video](https://youtu.be/gcwzWzC7gUA?si=OFmgDrREa3eesvPo) in which **DHH** showed how to install Omarchy and what it is.

Later I watched [this video](https://youtu.be/TcHY0AEd2Uw?si=omIh2Y6188X2w4yq) from official [Omarchy](https://omarchy.org) website and I was so impressed and decided to give it a try.

Basically, I didn't believe that it is possible to install something based on Arch Linux in a few minutes and it can actually work.

Until now, I'd only had experience with Ubuntu and was satisfied. What prompted me to try Omarchy was the many features preinstalled and prepared for web development, as well as *Hyprlnd* and *Tiling Windows.*

## Installation

I'd heard that installing *Arch Linux* was incredibly difficult. I'd also seen DHH install Omarchy on an instance in minutes, and it worked, even though Omarchy is built on Arch. I said, "I'll check it out," downloaded the Omarchy ISO image, burned it to a USB flash drive, and ran Framework 12 on my laptop.

I was very positively surprised because everything worked the first time and I saw the beautiful Omarchy desktop:

![Omarchy](x/images/omarchy/Pasted%20image%2020251009194547.png)

I thought, cool, but I definitely won't be able to connect to Wi-Fi... Well, it worked the first time, amazing!

![Omarchy](x/images/omarchy/Pasted%20image%2020251009194726.png)

BTW, you can see that the name of one of my Wi-Fi networks is "ReactJS"; it's from when I worked primarily as a frontend developer and I actually liked React. Nowadays, I don't like React as much as I did then, but I am too lazy to change the name of the network.

## First feelings

When it comes to aesthetics, I'm a bit of a weird person. On the one hand, I like simplicity, which is why I feel so comfortable in the Terminal. On the other hand, I'm also drawn to all sorts of graphical flourishes.

The Windows look is awful, I can't stand it. Mac OS looks better, but you have to ask Apple for permission to do anything, which is annoying.

And Omarchy is nice, it's beautiful. It's functional. It combines two worlds – TUI apps and Web Apps. DHH mentioned this in his talk, and I buy it:

![Omarchy](x/images/omarchy/Pasted%20image%2020251009201106.png)
On one side, Neovim in Terminal, full of old-school features, and on the other, Spotify, a modern invention. These two apps can be open side by side. Omarchy allows you to define your own apps, including native apps, web apps, and TUI apps.

Another example: on the left, Lazy Docker as a TUI app, and on the right, my website as a web app:

![Omarchy](x/images/omarchy/Pasted%20image%2020251009202000.png)
## Default apps

Omarchy comes with a ton of preinstalled software, especially for web developers. So immediately after install, I could use Neovim, Alactricity, and Docker. But not only apps for development. You can also find other useful apps installed by default, like Spotify, Signal, and Obsidian. On the other hand, I found apps that I don’t want to use, such as 1Password. The only minor issue is that you get a lot of stuff installed—some of which you might not like. It's not a big deal because you can easily uninstall it (which I'll talk about later).
## Keybindings

Omarchy focuses on using the keyboard as often as possible and provides several useful Key Bindings. SUPER key + Enter opens the terminal, SUPER + number from 1 to 5 switches the workspace. You can open many web and TUI apps using key bindings like SUPER + B, which opens the Browser. Key bindings are well documented. By pressing SUPER + K, you can see instant keybinding documentation:
![Omarchy](x/images/omarchy/Pasted%20image%2020251016091143.png)
You can also see them, edit, and add new bindings in the `~/.config/hypr/nindings.conf` file:

![Omarchy](x/images/omarchy/Pasted%20image%2020251016091357.png)

## Tilling windows

Tilling windows automatically arrange themselves in a grid or mosaic pattern on your screen, rather than overlapping freely. Instead of windows floating around independently, they tile to fill the available space without overlapping.

![Omarchy](x/images/omarchy/Pasted%20image%2020251016091751.png)

After just five minutes of using tiling windows, I knew I'd never go back to the "normal" windows I was used to from Ubuntu, *Windows*, or *Mac*. Thanks to Tilling Windows, I can manage my windows and feel more productive.

I can have multiple windows open simultaneously and keep them well-organized. When needed, I can enlarge the active window to full screen size by pressing F11. I can also move the selected window to a new workspace with SUPER + SHIFT + workspace number.

## Speed

I won't go into too much detail about the system's speed: on a laptop with an Intel i5, 32GB RAM, it works like Max Verstappen in a Formula 1 car.

Apart from that, I've never had anything freeze, and on my Ubuntu computer, it happens quite often (even several times a week)

## Daily usage

The system is stable; I haven't had a crash yet. What I usually do is development in Python and Django. So, I have a database open in Docker, a development server running, Neovim, a few terminals, Spotify, Signal, and other such trivia.
![Omarchy](x/images/omarchy/Pasted%20image%2020251010153456.png)

Besides, sometimes I just write (like now), I use Obsidian and a browser for research. It works very well for me, so I'd give it a 10/10. But it can't be that great. There's one thing that really annoys me. I'm talking about the display settings depending on whether I'm working on my laptop or an external screen. Another thing that annoys me, but not terribly, is the occasional problem with installing packages.
## Monitors issue

The first unpleasant thing is that every time I connect my laptop to an external monitor, I have to change the settings in `.config/hypr/monitors.conf`. If I don't do this, everything is too small on the external monitor. Similarly, when I disconnect the laptop from the monitor and want to work on the laptop screen, I have to change the monitor settings, because otherwise, everything on the screen is too large.

The second problem is that when I have my laptop connected to my computer, the workspaces don't function correctly. The thing is, you have five workspaces, and logic tells me that there should be separate workspaces for the external monitor and the laptop screen.

But the workspaces are shared, and it can get confusing. For example, you're on workspace 1 and you see something different on the laptop, such as a browser, and something else on the external monitor, such as a terminal.

When you switch workspaces, the changes are reflected on one screen, while the other screen remains unchanged.

De facto, it works like this: you have five workspaces on one screen and one on the other.

## Problem with installing packages e.g. firefox

I once ran into a problem where I couldn't install a package from the Omarcha repositories. Fortunately, I could do it using the AUR, so it wasn't a big deal.

![Omarchy](x/images/omarchy/Pasted%20image%2020251006071705.png)

## For whom Omarchy

As a car enthusiast, I can say that Omarchy is comparable to an Alfa Romeo. When everything works, you're thrilled, but when something starts breaking, you start to get annoyed. Fortunately, I didn't experience any major problems at first, so my experience has been very positive. I'd love to write a post next year about "Omarchy after a year of using it." In that time, I have a lot to catch up on and learn, especially about Arch Linux and Hyprl.

## Summary

So, yes, I plan to stick with this distro! It's the perfect distro for web developers and programmers. In my opinion, it's for people who already have Linux experience. If you're just starting out and migrating from Windows or Mac, I suggest starting with Omakub. It's a different distro from DHH, built on Ubuntu. It might be easier to get to grips with when starting out in the Linux world.

The biggest advantage of Omarchy is its appearance and functionality. It provides significant benefits in terms of work ergonomics. It provides default apps and setup for development. I would rate it 10/10, but due to an annoying issue with monitors, I need to be more strict and give it, let's say, 9!

---
*Published: 10/17/2025* #blog #linux #omarchy
