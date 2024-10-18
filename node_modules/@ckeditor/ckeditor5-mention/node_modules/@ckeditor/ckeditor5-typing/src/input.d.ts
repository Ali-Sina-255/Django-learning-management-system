/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
/**
 * @module typing/input
 */
import { Plugin } from '@ckeditor/ckeditor5-core';
/**
 * Handles text input coming from the keyboard or other input methods.
 */
export default class Input extends Plugin {
    /**
     * The queue of `insertText` command executions that are waiting for the DOM to get updated after beforeinput event.
     */
    private _compositionQueue;
    /**
     * @inheritDoc
     */
    static get pluginName(): "Input";
    /**
     * @inheritDoc
     */
    init(): void;
    /**
     * @inheritDoc
     */
    destroy(): void;
}
