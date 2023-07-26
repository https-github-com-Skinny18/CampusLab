import ldap
from django_auth_ldap.config import LDAPSearch

def autenticar(username, password):
    username = username.split('@')[0]
    result = buscarUsuario(username)
        
    if result:
        ldapdnread = result[0]['dn']
        conn = ldap.initialize("ldap://172.16.1.64")
        try:
            conn.simple_bind_s(ldapdnread, password)
            return result[0]
        except ldap.INVALID_CREDENTIALS:
            return False
    else:
        return False

def buscarUsuario(username):
    conn = ldap.initialize("ldap://172.16.1.64")
    conn.simple_bind_s("uid=nprof,ou=CPD,ou=Setores_Gerais,dc=UEA.EDU,dc=BR", "pueanprof")
    ldapusersearch = conn.search_s("dc=UEA.EDU,dc=BR", ldap.SCOPE_SUBTREE, "(uid=%s)" % username)
    result = []
    for dn, attrs in ldapusersearch:
        entry = {}
        entry['dn'] = dn
        for key, values in attrs.items():
            entry[key] = values[0]
        result.append(entry)
    return result
