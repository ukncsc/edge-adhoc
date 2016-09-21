Copyright (c) 2016 Crown Copyright (CERT-UK)  

Permission is hereby granted, free of charge, to use, copy, modify, merge, distribute and/or sub-licence the software together with any associated documentation provided that it is solely for your own internal use and subject to the following conditions:

(1)   The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.

(2)   THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN ANY ACTION FOR CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Adhoc Mod
Edge Mod is a Soltra Edge adapter that opens API access to Soltra Edge.

Further documentation and guidance on features provided by the adapter are detailed in the Wiki.

## Features

- Bulk search of objects
  - Address objects
  - Domain Name objects
  - Email objects
  - File objects
  - Socket objects
  - URI objects

## Status
The adapter is still under active development and as such shouldn't be considered a finished product.

## Installation
The adapter is currently aimed at version 2.8.1 of Soltra Edge. Other versions may work but your mileage may vary. The following is carried out as a Super User on the GUI whilst on the 'Admin > Adapters' page.

1. Upload and install the new adapter
2. Click on 'Restart Services' in the 'Restart Required' box

## Upgrade
Upgrading the adapter requires a few extra steps before following the installation instructions.

1. Click the red X to the right of the 'running' status on the certuk_mod line
2. Status will change to 'removing' but may get stuck, if so refresh the page
4. Click on 'Restart Services' in the 'Restart Required' box
5. Following the installation instructions


## Feedback
We would welcome feedback on this adapter and the functionality it provides. Please raise an issue on GitHub or email us at taxii[at]cert[dot]gov[dot]uk

## Thanks
Thanks to the folks at Soltra for building a great platform for us to build this adapter on.
