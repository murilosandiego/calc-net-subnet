#!/usr/bin/env python3
class MascaraInvalidaException(Exception):
    pass

class SubRedeInvalidaException(Exception):
    pass

import os

def criaLista(ip):
    listaIp = ip.split('.')
    if len(listaIp) != 4:
        raise ValueError
    return listaIp

def criaListaInteiro(ip):
    listaIp = [int(i) for i in ip]
    
    for i in listaIp:
        if i < 0 or i > 255:
            raise ValueError
    return listaIp

def calculaEnderecoRede(ip,mascara):
    rede = []
    for i in range(4):
        rede.append(ip[i] & mascara[i])
    return rede

def converteMascaraBinario(mascara):
    mMascara = ["{0:0>8b}".format(i) for i in mascara]
    wc = []
    l = ''.join(mMascara)
    l = list(l)
    for i in l:
        if i == '1':
            i = '0'
            wc.append(i)
        else:
            i = '1'
            wc.append(i)
    return wc

def validaMascara(mascara):
    for i in mascara:
        if (i != 128 and i != 192 and i != 224 and i != 240 and
            i != 248 and i != 252 and i != 254 and i != 255 and i != 0):
                raise MascaraInvalidaException

def manipulaWc(wc):
    wildcard = []
    wc1 = wc[0:8]
    wc2 = wc[8:16]
    wc3 = wc[16:24]
    wc4 = wc[24:32]

    wc1 = ''.join(wc1)
    wc2 = ''.join(wc2)
    wc3 = ''.join(wc3)
    wc4 = ''.join(wc4)
    wildcard.append(binarioParaDecimal(wc1))
    wildcard.append(binarioParaDecimal(wc2))
    wildcard.append(binarioParaDecimal(wc3))
    wildcard.append(binarioParaDecimal(wc4))
    return wildcard
        
def binarioParaDecimal(wc):
    return int(wc,2)
          
def manipulaIP(ip):
    mIp = criaLista(ip)
    mIp = criaListaInteiro(mIp)
    return mIp

def manipulaMascara(mascara):
    mMascara = []
    mascara = int(mascara)

    if mascara < 1 or mascara > 32:
        raise MascaraInvalidaException
    
    for i in range(32):
        if i < mascara:
            mMascara.append('1')
        else:
            mMascara.append('0')

    mMascara = manipulaWc(mMascara)
    mMascara = criaListaInteiro(mMascara)
    validaMascara(mMascara)
    return mMascara

def enderecoRede(ip,mascara):
    return calculaEnderecoRede(ip,mascara)

def enderecoWildcard(mascara):
    wc = converteMascaraBinario(mascara)
    return manipulaWc(wc)

def enderecoBroadcast(ip,wc):
    bc = []  
    for i in range(4):
        bc.append(ip[i] | wc[i])
    return bc

def hostMinimo(rede,mascara):
    if mascara[3] == 255 or mascara[3] == 254:
        host = rede
    else:
        host = [rede[0],rede[1],rede[2],rede[3]+1]
    return host

def hostMaximo(bc,mascara):
    if mascara[3] == 255 or mascara[3] == 254:
        host = bc
    else:
        host = [bc[0],bc[1],bc[2],bc[3]-1]
    return host

def estilizaIP(ip):
    mIp = str(ip)
    mIp = mIp.replace(',','.')
    mIp = mIp.replace('[','')
    mIp = mIp.replace(']','')
    return mIp
    
def calculaSubRede(rede,wc,bc,mascara):   
    mCIRD = input('\nInforme a máscara da sub-rede , ex: 26: ')
    subMascara = manipulaMascara(mCIRD)

    if mascara > subMascara:
        raise SubRedeInvalidaException
    
    wc = enderecoWildcard(subMascara)
    rede = enderecoRede(rede,subMascara)
    subBc = enderecoBroadcast(rede,wc)
    print('\nSub-Redes')
    print('-'*47,'\nMascara:\t',estilizaIP(subMascara),'=',mCIRD,'\n\nEndereço Rede:\t',
          estilizaIP(rede),'/',mCIRD,'\nBroadcast:\t',estilizaIP(subBc),
          '\nHost Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
          estilizaIP(hostMaximo(subBc,subMascara)))
    qtd = 1
    while True:
        if subBc[3] < 255:
            if subBc == bc:
                    break
            rede = [subBc[0],subBc[1],subBc[2],subBc[3]+1]
            subBc = enderecoBroadcast(rede,wc)
            print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
            print('Broadcast:\t',estilizaIP(subBc))
            print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
            qtd += 1
            if subBc == bc:
                break
            if subBc[3] == 255:
                subBc[3] = 0
                rede = [subBc[0],subBc[1],subBc[2]+1,subBc[3]]
                subBc = enderecoBroadcast(rede,wc)
                print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
                print('Broadcast:\t',estilizaIP(subBc))
                print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
                qtd += 1
                if subBc == bc:
                    break
        elif subBc[2] < 255:
            if subBc == bc:
                break
            subBc[3] = 0
            rede = [subBc[0],subBc[1],subBc[2]+1,subBc[3]]
            subBc = enderecoBroadcast(rede,wc)
            print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
            print('Broadcast:\t',estilizaIP(subBc))
            print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
            qtd += 1
            if subBc == bc:
                break
            if subBc[2] == 255:
                subBc[2] = 0
                subBc[3] = 0
                rede = [subBc[0],subBc[1]+1,subBc[2],subBc[3]]
                subBc = enderecoBroadcast(rede,wc)
                print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
                print('Broadcast:\t',estilizaIP(subBc))
                print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
                qtd += 1
                if subBc == bc:
                    break
        elif subBc[1] < 255:
            if subBc == bc:
                break
            subBc[3] = 0
            subBc[2] = 0
            rede = [subBc[0],subBc[1]+1,subBc[2],subBc[3]]
            subBc = enderecoBroadcast(rede,wc)
            print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
            print('Broadcast:\t',estilizaIP(subBc))
            print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
            qtd += 1
            if subBc == bc:
                break
            if subBc[1] == 255:
                subBc[1] = 0
                subBc[3] = 0
                subBc[2] = 0
                rede = [subBc[0]+1,subBc[1],subBc[2],subBc[3]]
                subBc = enderecoBroadcast(rede,wc)
                print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
                print('Broadcast:\t',estilizaIP(subBc))
                print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
                qtd += 1
                if subBc == bc:
                    break
        elif subBc[0] < 255:
            if subBc == bc:
                break
            subBc[3] = 0
            subBc[2] = 0
            subBc[1] = 0
            rede = [subBc[0]+1,subBc[1],subBc[2],subBc[3]]
            subBc = enderecoBroadcast(rede,wc)
            print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
            print('Broadcast:\t',estilizaIP(subBc))
            print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
            qtd += 1
            if subBc == bc:
                break
            if subBc[0] == 255:
                subBc[0] = 0
                subBc[3] = 0
                subBc[2] = 0
                subBc[1] = 0
                rede = [subBc[0],subBc[1],subBc[2],subBc[3]]
                subBc = enderecoBroadcast(rede,wc)
                print('\nEndereço Rede:\t',estilizaIP(rede),'/',mCIRD,)
                print('Broadcast:\t',estilizaIP(subBc))
                print('Host Mínimo:\t',estilizaIP(hostMinimo(rede,subMascara)),'\nHost Máximo:\t',
                  estilizaIP(hostMaximo(subBc,subMascara)))
                qtd += 1
                if subBc == bc:
                    break
    print('\nQtd Sub-Redes:\t',qtd)

def separaIPMascara(ipMascara):
    ipMascara = ipMascara.split('/')
    if len(ipMascara) != 2:
        raise ValueError
    ip = ipMascara[0]
    mascara = ipMascara[1]
    return ip,mascara

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ipStr = input('Informe o endereço IP e Máscara da rede, ex: 192.168.0.1/24: ')

        try:
            ip, mCIRD = separaIPMascara(ipStr)
            ip = manipulaIP(ip)
            mascara = manipulaMascara(mCIRD)
            rede = enderecoRede(ip,mascara)
            wc = enderecoWildcard(mascara)
            bc = enderecoBroadcast(ip,wc)
            hmin = hostMinimo(rede,mascara)
            hmax = hostMaximo(bc,mascara)
            
            redeStr = estilizaIP(rede)
            bcStr = estilizaIP(bc)
            hminStr = estilizaIP(hmin)
            hmaxStr = estilizaIP(hmax)
            print('\nIP:\t\t',estilizaIP(ip),'\nMáscara:\t',estilizaIP(mascara),'=',mCIRD, '\n\nEndereço Rede:\t',redeStr,'/',mCIRD,'\nBroadcast:\t',bcStr,
              '\nHost Mínimo:\t',hminStr,'\nHost Máximo:\t',hmaxStr)
            
            subResposta = input('\nDeseja calcular Sub-Redes? (S- Sim, N - Não): ')
            if subResposta == 'S' or subResposta == 's':
                calculaSubRede(rede,wc,bc,mascara)
                
        except ValueError:
            print('\nEndereço inválido! favor informar IP e máscara válidos')
        except SubRedeInvalidaException:
            print('\nErro! sua Sub-Rede deve está contida em sua rede')
        except MascaraInvalidaException:
            print('\nMáscara Invalida! favor informar uma máscara válida')
        except Exception as e:
            print(e)

        resposta = input('\nDeseja fazer outro cálculo? (S- Sim, N - Não): ')
        if resposta == 'N' or resposta == 'n':
            break
if __name__ == '__main__':
    main()
