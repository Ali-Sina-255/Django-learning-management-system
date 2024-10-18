/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
import { icons } from '@ckeditor/ckeditor5-core';
import ButtonView from './buttonview.js';
import ButtonLabelView from './buttonlabelview.js';
import IconView from '../icon/iconview.js';
import View from '../view.js';
import '../../theme/components/button/listitembutton.css';
/**
 * Button that is used as dropdown list item entry.
 */
export default class ListItemButtonView extends ButtonView {
    /**
     * @inheritDoc
     */
    constructor(locale, labelView = new ButtonLabelView()) {
        super(locale, labelView);
        /**
         * Holds the view for the check icon of a button list item.
         */
        this._checkIconHolderView = new CheckIconHolderView();
        this.set({
            hasCheckSpace: false,
            _hasCheck: this.isToggleable
        });
        const bind = this.bindTemplate;
        this.extendTemplate({
            attributes: {
                class: [
                    'ck-list-item-button',
                    bind.if('isToggleable', 'ck-list-item-button_toggleable')
                ]
            }
        });
        this.bind('_hasCheck').to(this, 'hasCheckSpace', this, 'isToggleable', (hasCheckSpace, isToggleable) => hasCheckSpace || isToggleable);
    }
    /**
     * @inheritDoc
     */
    render() {
        super.render();
        if (this._hasCheck) {
            this.children.add(this._checkIconHolderView, 0);
        }
        this._watchCheckIconHolderMount();
    }
    /**
     * Renders the check icon if the button is toggleable.
     */
    _watchCheckIconHolderMount() {
        this._checkIconHolderView
            .bind('isOn')
            .to(this, 'isOn', value => this.isToggleable && value);
        this.on('change:_hasCheck', (evt, propertyName, hasCheck) => {
            const { children, _checkIconHolderView } = this;
            if (hasCheck) {
                children.add(_checkIconHolderView, 0);
            }
            else {
                children.remove(_checkIconHolderView);
            }
        });
    }
}
export class CheckIconHolderView extends View {
    /**
     * @inheritDoc
     */
    constructor() {
        super();
        /**
         * The view for the check icon of the button list item.
         */
        this._checkIconView = this._createCheckIconView();
        const bind = this.bindTemplate;
        this.children = this.createCollection();
        this.set('isOn', false);
        this.setTemplate({
            tag: 'span',
            children: this.children,
            attributes: {
                class: [
                    'ck',
                    'ck-list-item-button__check-holder',
                    bind.to('isOn', isOn => isOn ? 'ck-on' : 'ck-off')
                ]
            }
        });
    }
    /**
     * @inheritDoc
     */
    render() {
        super.render();
        if (this.isOn) {
            this.children.add(this._checkIconView, 0);
        }
        this._watchCheckIconMount();
    }
    /**
     * Renders the check icon if the button is toggleable.
     */
    _watchCheckIconMount() {
        this.on('change:isOn', (evt, propertyName, isOn) => {
            const { children, _checkIconView } = this;
            if (isOn && !children.has(_checkIconView)) {
                children.add(_checkIconView);
            }
            else if (!isOn && children.has(_checkIconView)) {
                children.remove(_checkIconView);
            }
        });
    }
    /**
     * Creates a check icon view.
     */
    _createCheckIconView() {
        const iconView = new IconView();
        iconView.content = icons.check;
        iconView.extendTemplate({
            attributes: {
                class: 'ck-list-item-button__check-icon'
            }
        });
        return iconView;
    }
}
