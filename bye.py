import time

if __name__ == '__main__':

    for thanks in [' aux dévelopeurs de django', ' à jetbrains pour son excellent IDE (+ vim pour les acharnés)', 'à PortSwigger pour son '
                                                                                        'aimable autorisation '
                                                                                        'd\'utiliser BURP',
                   ' à vous qui regardez cette vidéo', ' pour votre curiosité', 'et vous pouvez vous abonner pour être notifié des prochaines '
                                                       'vidéos']:
        print('#' * 50)
        print(f'Merci {thanks}\n')
        time.sleep(3)
