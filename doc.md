wss://stream.binance.com:9443/ws/btcusdt@trade
https://python-binance.readthedocs.io/en/latest/

wss://stream.binance.com:9443/ws/btcusdt@kline_5m


wss://stream.binance.com:9443

{
    "e":"trade",
    "E":1686222917126,
    "s":"BTCUSDT",
    "t":3137907815,
    "p":"26468.33000000",
    "q":"0.00175000",
    "b":21379315178,
    "a":21379316459,
    "T":1686222917126,
    "m":true,
    "M":true
}

{"e":"kline",
"E":1686223366821,
"s":"BTCUSDT",
"k":{"t":1686223200000,"T":1686223499999,"s":"BTCUSDT","i":"5m","f":3137910477,"L":3137911460,"o":"26442.93000000","c":"26446.23000000","h":"26446.23000000","l":"26442.93000000","v":"21.22022000","n":984,"x":false,"q":"561153.03370100","V":"14.04272000","Q":"371351.74227240","B":"0"}}


#

Goal for Observer Capital terminal

- Order execution and basis will/should be very similar to every other terminal, something like Tealstreet, Tuleep, ect but with our own twists if we want them

Perks and differences of having our own terminal would be 
 - Webhooks/integrations of Orion Data and Coinalyze. Also some integrations of VeloData but I need to look more into that before anything, so ignore that for now
 - Full customization of whatever we want, its our terminal, our playground, freedom
 - Communication with our bots through our terminal, if or when we have bots
 - (optional) Messaging service to privately/securely message other OB capital users on the terminal, so we can fucking ditch discord. Useful for trade ideas and quick and easy access to each other during large events. Also we could make it look like a cool af chatroom, idk im dreaming
 - (late game, ignore for now) Sub account aggregator, I will explain this more when we get VIP 1 on Binance, but think of it as a master API key for multiple Binance accounts (subaccounts) so we can circumvent maximum order sizes and leverage sizes on coins.
 There isn't a terminal that I know of with this feature

If all goes well and the terminal is massively useful, we could release/sell a *less featured* version to the public and farm referrals to major exchanges for some nice passive income. There are more uses to this thing than just for us personally