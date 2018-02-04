from logging import getLogger
from os import makedirs, environ
from pathlib import Path
from json import load, dump
from sys import stdout
from horetu import OutputFile

CONFIG = Path(environ['HOME']) / '.securepolling.json'
logger = getLogger(__name__)

def create(registrar, identity, config=CONFIG, *, force=False):
    '''
    Create an identity.

    Add random salt to identity to prevent others from querying registrars'
    servers on users' behalf, when identity is their real name.

    :param registrar: the registrar's server URL
    :param identity: A unique string with information that the registrar will
    use to verify user identity in person.
    '''
    if config.exists() and not force:
        raise ValueError('Configuration already exists: %s' % config)

    data = {
        'registrar': registrar,
        'identity': identity,
    }

    if config == '-':
        fp = stdout
    else:
        p = Path(config)
        makedirs(p.parent)
        fp = p.open('w')
    dump(data, fp)
    fp.close()

def tally_servers(*tally_servers, config: Path=CONFIG):
    '''
    Add tally servers to your configuration.

    :param tally_servers: tally servers
    '''
    with config.open() as fp:
        data = load(fp)
    if 'tally_servers' not in data:
        data['tally_servers'] = []
    for tally_server in tally_servers:
        if tally_server not in data['tally_servers']:
            data['tally_servers'].append(tally_server)
    with config.open('w') as fp:
        dump(data, fp)

def generate_keypair(config: Path=CONFIG):
    '''
    Generates a new keypair and save it.
    If a keypair already exists with a valid registrar signature, return an
    error, otherwise overwrite an existing signature.
    '''

def _send_blinded_key(registrar, identity):
    '''
    App generates and stores a random salt. The client acquires a public subkey
    from the registrar. The app uses that public subkey to generate a blinded
    version of the user's public key, then sends the blinded version to the
    registrar.
    '''

def _signature_valid(registrar, identity):
    '''
    Return true if the locally-stored registrar signature is valid.
    Return false if the registrar signature is expired or not present.
    '''

def _get_signature(registrar, identity):
    '''
    Get the registrar signature for the given identity. This function will
    attempt to retrieve the registrar's signature of user's blinded key, unblind
    it using the stored salt, store the result (a signature of user's public
    key) locally, and return true. If there is no valid signature data supplied
    by the registrar, it will return false.
    '''

def screed_add(*messages, config: Path=CONFIG):
    '''
    Add messages to the local screed.
    '''
    with config.open() as fp:
        data = load(fp)
    data['screed'].extend(messages)
    with config.open('w') as fp:
        dump(data, fp)

def screed_remove(*indexes: int, config: Path=CONFIG):
    '''
    Remove messages from the local screed.
    '''
    with config.open() as fp:
        data = load(fp)
    for i in indexes:
        data['screed'].remove(i)
    with config.open('w') as fp:
        dump(data, fp)

def screed_list(config: Path=CONFIG):
    '''
    List the current messages in the local screed, along with their indexes.
    '''
    with config.open() as fp:
        data = load(fp)
    for i, message in enumerate(data['screed']):
        yield '%05d   %s' % (i, message)

def screed_upload(config: Path=CONFIG):
    '''
    Upload the user's local screed to the registrar. If there is no valid
    signature for the user's registrar, or the server refuses to accept, or
    can't be reached, raise an error.
    '''
    with config.open() as fp:
        data = load(fp)
    logger.critical('Upload screed to %(registrar)s' % data)