/*
 * Copyright (C) by Daniel Molkentin <danimo@owncloud.com>, ownCloud Inc.
 */

#ifndef CERNBOX_THEME_H
#define CERNBOX_THEME_H

#include "theme.h"

#include <QString>
#include <QDebug>
#include <QPixmap>
#include <QIcon>
#include <QApplication>


namespace Mirall {

class CernBoxTheme : public Theme
{
public:
    CernBoxTheme() {};

    QString configFileName() const { return QLatin1String("cernbox.cfg"); }
    QIcon   trayFolderIcon( const QString& ) const { return themeIcon( QLatin1String("cernbox-icon") ); }
    QIcon   folderDisabledIcon() const { return themeIcon( QLatin1String("state-pause") ); }
    QIcon   applicationIcon() const { return themeIcon( QLatin1String("cernbox-icon") ); }
    QString defaultServerFolder() const { return  QLatin1String("/home"); }
// QString defaultServerFolder() const Q_DECL_OVERRIDE { return QLatin1String("cernbox"); }
    QString overrideServerUrl() const { return QLatin1String("https://cernbox.cern.ch/cernbox/desktop"); }
    QPixmap wizardHeaderLogo() const { return applicationIcon().pixmap(64); }
    bool singleSyncFolder() { return true; }

  

};

} // namespace mirall

#endif // CERNBOX_THEME_H
