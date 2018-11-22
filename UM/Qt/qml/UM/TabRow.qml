// Copyright (c) 2018 Ultimaker B.V.
// Uranium is released under the terms of the LGPLv3 or higher.

import QtQuick 2.0
import QtQuick.Controls 2.0
import UM 1.2 as UM

/*
 * Wrapper around TabBar that uses our theming and more sane defaults.
 */
TabBar
{
    id: base

    width: parent.width
    height: 50

    spacing: UM.Theme.getSize("default_margin").width //Space between the tabs.
}