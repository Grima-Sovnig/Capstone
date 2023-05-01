import pysftp;

cnopts = pysftp.CnOpts();
cnopts.hostkeys = None;

cinfo = {
    'host':'sftp.alexpro.net',
    'username':'team6',
    'password':r'sftpPipeline',
    'priv_key':'c:\\path\\to\\my\\ssh.key',
    'priv_key_pass':'sftpPipeline',
    'port':22,
    'cnopts':cnopts,
    'default_path' : 'CompanyProjectName'
}

with pysftp.Connection(cinfo) as sftpConnect:
    # sftp.put( 'file_path', 'optional_target_directory' );
    # sftp.close();
